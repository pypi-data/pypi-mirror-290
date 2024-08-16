# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import json
import time
from typing import (
    Any,
    Awaitable,
    Callable,
    AsyncGenerator,
    ParamSpecArgs,
    ParamSpecKwargs,
    Optional,
    cast,
)

import openai
from lastmile_eval.rag.debugger.api import LastMileTracer
from openai.resources.chat import (
    AsyncChat,
    AsyncCompletions,
)
from openai.resources.embeddings import (
    AsyncEmbeddings,
)
from openai.types import CreateEmbeddingResponse
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
)
from openai import AsyncStream

from ..utils import (
    Wrapper,
    json_serialize_anything,
)

from .shared import (
    add_rag_event_with_output,
    parse_params,
    flatten_json,
)


class AsyncOpenAIWrapper(Wrapper[openai.AsyncOpenAI]):
    def __init__(
        self,
        client: openai.AsyncOpenAI,
        tracer: LastMileTracer,
    ):
        super().__init__(client)
        self._tracer: LastMileTracer = tracer
        self.embeddings = AsyncEmbeddingWrapper(
            client.embeddings, self._tracer
        )
        self.chat = AsyncChatWrapper(client.chat, self._tracer)


class AsyncEmbeddingWrapper(Wrapper[AsyncEmbeddings]):
    def __init__(self, embedding: AsyncEmbeddings, tracer: LastMileTracer):
        super().__init__(embedding)
        self._embedding = embedding
        self._tracer = tracer

    async def create(
        self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs
    ) -> CreateEmbeddingResponse:
        return await self._create_impl(*args, **kwargs)

    async def _create_impl(
        self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs
    ) -> CreateEmbeddingResponse:
        params = parse_params(kwargs)

        with self._tracer.start_as_current_span(
            "async-embedding-create"
        ) as span:
            raw_response = await self._embedding.create(*args, **kwargs)
            log_response = (
                raw_response
                if isinstance(raw_response, dict)
                else raw_response.model_dump()
            )
            span.set_attributes(
                {
                    "tokens": log_response["usage"]["total_tokens"],
                    "prompt_tokens": log_response["usage"]["prompt_tokens"],
                    "embedding_length": len(
                        log_response["data"][0]["embedding"]
                    ),
                    **flatten_json(params),
                },
            )
            return raw_response


class AsyncChatWrapper(Wrapper[AsyncChat]):
    def __init__(self, chat: AsyncChat, tracer: LastMileTracer):
        super().__init__(chat)
        self.completions = AsyncCompletionsWrapper(chat.completions, tracer)


class AsyncCompletionsWrapper(Wrapper[AsyncCompletions]):
    def __init__(self, completions: AsyncCompletions, tracer: LastMileTracer):
        super().__init__(completions)
        self.create_fn: Callable[  # TODO: Map this directly to OpenAI package
            ...,
            Awaitable[ChatCompletion | AsyncStream[ChatCompletionChunk]],
        ] = completions.create
        self._tracer = tracer

    async def create(
        self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        response = self._create_impl(*args, **kwargs)

        stream = kwargs.get("stream", False)
        if not stream:
            non_streaming_response_value = cast(
                ChatCompletion, await anext(response)
            )
            return non_streaming_response_value
        return cast(AsyncStream[ChatCompletionChunk], response)

    async def _create_impl(
        self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs
    ) -> AsyncGenerator[
        ChatCompletion  # for "non-streaming" only that we parse later
        | ChatCompletionChunk,
        Any,
    ]:
        params = parse_params(kwargs)
        if "input" in params:
            # Rename "input" to "messages" to avoid confusion with rag event
            # or span inputs
            params["messages"] = params["input"]
            del params["input"]
        params_flat = flatten_json(params)

        messages: list[ChatCompletionMessageParam | ChatCompletionMessage] = kwargs["messages"] if "messages" in kwargs else []  # type: ignore
        user_prompt: Optional[str] = None
        for message in reversed(messages):
            if isinstance(message, ChatCompletionMessage):
                if message.role == "user":
                    if isinstance(message["content"], str):
                        user_prompt = message["content"]
                    break
            elif isinstance(message, dict):
                if message.get("role") == "user":
                    # TODO (rossdan): Handle Iterable[ChatCompletionContentPartParam] use case
                    if isinstance(message["content"], str):
                        user_prompt = message["content"]
                    break
        rag_event_serialized = json_serialize_anything(params)

        with self._tracer.start_as_current_span(
            "async-chat-completion-create"
        ) as span:
            span.set_attributes(flatten_json(params))
            start = time.time()
            raw_response = await self.create_fn(*args, **kwargs)
            if isinstance(raw_response, AsyncStream):

                async def gen():
                    first = True
                    accumulated_text = None
                    function_name = None
                    async for item in raw_response:
                        if first:
                            span.set_attribute(
                                "time_to_first_token", time.time() - start
                            )
                            first = False
                        if isinstance(item, ChatCompletionChunk):  # type: ignore
                            # Ignore multiple responses for now,
                            # will support in future PR, by looking at the index in choice dict
                            # We need to also support tool call handling (as well as tool
                            # call handling streaming, which we never did properly):
                            # https://community.openai.com/t/has-anyone-managed-to-get-a-tool-call-working-when-stream-true/498867
                            choice = item.choices[
                                0
                            ]  # TODO: Can be multiple if n > 1

                            if choice and choice.delta:
                                if choice.delta.content is not None:
                                    accumulated_text = (
                                        accumulated_text or ""
                                    ) + choice.delta.content
                                elif choice.delta.tool_calls:
                                    function_chunk = choice.delta.tool_calls[
                                        0
                                    ].function
                                    if function_chunk.name is not None:
                                        function_name = function_chunk.name
                                    accumulated_text = (
                                        accumulated_text or ""
                                    ) + (function_chunk.arguments or "")
                        yield item

                    if accumulated_text is not None:
                        # TODO: Save all the data inside of the span instead of
                        # just the output text content
                        if function_name is None:
                            span.set_attribute(
                                "output_content", accumulated_text
                            )
                        else:
                            span.set_attribute(
                                "output_arguments", accumulated_text
                            )
                            span.set_attribute(
                                "output_function_name", function_name
                            )
                    if function_name is not None:
                        self._tracer.log_tool_call_event(
                            query=user_prompt or rag_event_serialized,
                            tool_name=function_name,
                            tool_arguments=json.loads(
                                accumulated_text or "{}"
                            ),
                            span=span,
                            metadata=json.loads(rag_event_serialized),
                        )
                    else:
                        add_rag_event_with_output(
                            self._tracer,
                            "chat_completion_create_stream",
                            span,
                            input=user_prompt or rag_event_serialized,
                            output=accumulated_text,
                            event_data=json.loads(rag_event_serialized),
                            # TODO: Support tool calls
                            # TODO: Use enum from lastmile-eval package
                            span_kind="query",
                        )

                async for chunk in gen():
                    yield chunk

            # Non-streaming part
            else:
                log_response = (
                    raw_response
                    if isinstance(raw_response, dict)
                    else raw_response.model_dump()
                )
                span.set_attributes(
                    {
                        "tokens": log_response["usage"]["total_tokens"],
                        "prompt_tokens": log_response["usage"][
                            "prompt_tokens"
                        ],
                        "completion_tokens": log_response["usage"][
                            "completion_tokens"
                        ],
                        "choices": json_serialize_anything(
                            log_response["choices"]
                        ),
                        **params_flat,
                    }
                )
                try:
                    # TODO (rossdan): Handle responses where n > 1
                    output_message = log_response["choices"][0]["message"]
                    if (
                        "tool_calls" in output_message
                        and output_message["tool_calls"]
                    ):
                        # TODO (rossdan): Handle responses where n > 1
                        tool_call = output_message["tool_calls"][0]
                        tool_call_type = tool_call["type"]
                        if tool_call_type == "function":
                            tool_call_data = tool_call[tool_call_type]
                            self._tracer.log_tool_call_event(
                                query=user_prompt or rag_event_serialized,
                                tool_name=tool_call_data["name"],
                                tool_arguments=tool_call_data["arguments"],
                                span=span,
                                metadata=json.loads(rag_event_serialized),
                            )
                        else:
                            self._tracer.log_span_event(
                                input=user_prompt or rag_event_serialized,
                                output="",
                                event_data=json.loads(rag_event_serialized),
                            )
                    else:
                        add_rag_event_with_output(
                            self._tracer,
                            "chat_completion_create",
                            span,
                            input=user_prompt or rag_event_serialized,
                            output=output_message["content"],
                            event_data=json.loads(rag_event_serialized),
                            # TODO: Support tool calls
                            # TODO: Use enum from lastmile-eval package
                            span_kind="query",
                        )
                except Exception as e:
                    # TODO log this
                    pass

                # Python is a clown language and does not allow you to both
                # yield and return in the same function (return just exits
                # the generator early), and there's no explicit way of
                # making this obviously because Python isn't statically typed
                #
                # We have to yield instead of returning a generator for
                # streaming because if we return a generator, the generator
                # does not actually compute or execute the values until later
                # and at which point the span has already closed. Besides
                # getting an an error saying that there's no defined trace id
                # to log the rag events, this is just not good to do because
                # what's the point of having a span to trace data if it ends
                # prematurely before we've actually computed any values?
                # Therefore we must yield to ensure the span remains open for
                # streaming events.
                #
                # For non-streaming, this means that we're still yielding the
                # "returned" response and we just process it at callsites
                # using return next(response)
                yield raw_response
