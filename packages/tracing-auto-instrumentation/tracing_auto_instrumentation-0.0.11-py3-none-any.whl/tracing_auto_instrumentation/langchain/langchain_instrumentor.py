from typing import Any, Dict, Callable, Collection, Optional, Type, Union
from collections import defaultdict

import json
import logging

# LangChain
from langchain_core.callbacks import BaseCallbackManager
from langchain_core.tracers.schemas import Run

from openinference.instrumentation.langchain._tracer import (
    EMBEDDING_MODEL_NAME,
    INPUT_VALUE,
    LLM_INPUT_MESSAGES,
    LLM_INVOCATION_PARAMETERS,
    LLM_MODEL_NAME,
    LLM_PROMPT_TEMPLATE,
    LLM_PROMPT_TEMPLATE_VARIABLES,
    LLM_TOKEN_COUNT_COMPLETION,
    LLM_TOKEN_COUNT_PROMPT,
    LLM_TOKEN_COUNT_TOTAL,
    OUTPUT_VALUE,
    RETRIEVAL_DOCUMENTS,
    TOOL_DESCRIPTION,
    TOOL_NAME,
    OpenInferenceTracer,
    _as_utc_nano,
    _update_span,
)

# OpenInference
from openinference.instrumentation.langchain.package import _instruments
from openinference.instrumentation.langchain.version import __version__

# OpenTelemetry
from opentelemetry import context as context_api

from opentelemetry.context import _SUPPRESS_INSTRUMENTATION_KEY
from opentelemetry.sdk.trace import Span

from opentelemetry.instrumentation.instrumentor import (
    BaseInstrumentor,
)  # type: ignore

# wrapt
from wrapt import wrap_function_wrapper

# lastmile internals
from lastmile_eval.rag.debugger.api import (
    LastMileTracer,
    RetrievedChunk,
)  # TODO(b7r6): fix typing...


# logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer

from ..utils import DEFAULT_TRACER_NAME_PREFIX


# When saving metadata for an event, refine the key to more readable / usable value
# We can do this safely for all keys within a specific event since there should be no
# overlap between keys in different events (e.g. EMBEDDING_MODEL_NAME and LLM_MODEL_NAME)
def refine_metadata_key(key: str) -> str:
    if key == EMBEDDING_MODEL_NAME or key == LLM_MODEL_NAME:
        return "model"

    if key == LLM_PROMPT_TEMPLATE:
        return "prompt_template"

    if key == LLM_PROMPT_TEMPLATE_VARIABLES:
        return "prompt_template_variables"

    if key == LLM_TOKEN_COUNT_PROMPT:
        return "token_count_prompt"

    if key == LLM_TOKEN_COUNT_COMPLETION:
        return "token_count_completion"

    if key == LLM_TOKEN_COUNT_TOTAL:
        return "token_count_total"

    return key


class LangChainInstrumentor(BaseInstrumentor):
    """
    This is a callback handler for automatically instrumenting with
    LangChain. Here's how to use it:

    ```
    from lastmile_eval.rag.debugger.tracing.auto_instrumentation import LangChainInstrumentor
    LangChainInstrumentor().instrument()
    # Do regular LangChain calls as usual
    ```
    """

    def __init__(
        self,
        project_name: Optional[str] = None,
        lastmile_api_token: Optional[str] = None,
    ) -> None:
        super().__init__()

        self._tracer: LastMileTracer = get_lastmile_tracer(
            tracer_name=project_name
            or (DEFAULT_TRACER_NAME_PREFIX + " - LangChain"),
            lastmile_api_token=lastmile_api_token,
            project_name=project_name,
        )

    def get_tracer(self) -> LastMileTracer:
        return self._tracer

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:
        wrap_function_wrapper(
            module="langchain_core.callbacks",
            name="BaseCallbackManager.__init__",
            wrapper=_BaseCallbackManagerInit(
                # TODO: Define our own LastMileTracerLangChainTracer to
                # inherit OpenInferenceTracer. Override _end_trace to save
                # span kind in our own field
                tracer=self._tracer,
                cls=_LastMileLangChainTracer,
            ),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass


# TODO(b7r6): this is an inherently brittle design because of the overrides on private
class _LastMileLangChainTracer(OpenInferenceTracer):
    def _end_trace(self, run: Run) -> None:

        self.run_map.pop(str(run.id), None)

        if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
            return

        span = self._spans_by_run.pop(run.id, None)

        if not span:
            return

        self._handle_span(run, span)

    def _handle_span(self, run: Run, span: Span):
        assert isinstance(self._tracer, LastMileTracer)

        # update span
        try:
            _update_span(span, run)
        except Exception:
            logger.exception("Failed to update span with run data.")

        span_kind = str(
            "agent" if "agent" in run.name.lower() else (run.run_type)
        )

        if _should_process(span_kind):
            span_attributes: dict[str, Any] = span._attributes  # type: ignore
            serializable_payload: Dict[str, Any] = {}

            for key, value in span.attributes.items():
                serializable_payload[refine_metadata_key(str(key))] = value

            if "retriever" == span_kind:
                # doc_info contains as key the index of the document and value the
                # info of the document
                # Example: {0: {'id': 'doc1', 'score': 0.5, 'content': 'doc1 content'}}
                doc_info: defaultdict[int, dict[str, Union[str, float]]] = (
                    defaultdict(dict)
                )
                for key, value in span_attributes.items():
                    if RETRIEVAL_DOCUMENTS in key:
                        # Example of key would be retrieval.documents.1.document.content
                        key_parts = key.split(".")
                        doc_index: int = -1
                        for part in key_parts:
                            if part.isnumeric():
                                doc_index = int(part)
                        if doc_index == -1:
                            continue

                        # info will be either "metadata", "content" (score not included)
                        info_type = key.split(".")[-1]
                        doc_info[doc_index][info_type] = value

                # build list of retrieved nodes
                retrieved_chunks: list[RetrievedChunk] = []
                # Sort the keys (document index) to add them in correct order
                # to the retrieved nodes array
                for i, info_dict in enumerate(
                    dict(sorted(doc_info.items())).values()
                ):
                    # OpenTelemetry does not allow dict values so metadata
                    # is stored as a string and we need to json load it
                    source = json.loads(info_dict.get("metadata", "{}")).get(
                        "source", "file not found"
                    )
                    retrieved_chunks.append(
                        RetrievedChunk(
                            id=f"idx-{i}-{source}",  # node id is not included in LangChain
                            retrieval_score=-1.0,  # score is not included LangChain retrieve event
                            content=str(info_dict["content"]),
                        )
                    )

                self._tracer.log_retrieval_event(
                    query=span_attributes.get(INPUT_VALUE, ""),
                    retrieved_data=retrieved_chunks,
                    span=span,
                    metadata={"top_k": len(retrieved_chunks)},
                )
            elif "tool" == span_kind:
                tool_name = span_attributes.get(TOOL_NAME)
                self._tracer.log_tool_call_event(
                    event_name=tool_name,
                    query=span_attributes.get(INPUT_VALUE, ""),
                    tool_name=tool_name,
                    span=span,
                    metadata={
                        "description": span_attributes.get(TOOL_DESCRIPTION),
                    },
                )
            elif "llm" == span_kind:
                resolved_prompt = None
                output = span_attributes[OUTPUT_VALUE]

                metadata: dict[str, Any] = {}

                # Un-nest completion params from llm.invocation_parameters
                completion_params: dict[str, Any] | str = span_attributes.get(
                    LLM_INVOCATION_PARAMETERS, {}
                )

                if isinstance(completion_params, str):
                    try:
                        completion_params = json.loads(completion_params)
                    except json.JSONDecodeError:
                        logger.exception(
                            "Failed to parse completion params as JSON"
                        )
                        completion_params = {}

                if isinstance(completion_params, dict):
                    metadata.update(completion_params)

                # Wow what a hack just to deal with WatsonxLLM
                if "WatsonxLLM" in span._name:
                    # Handle Watson only!
                    prompts = json.loads(span_attributes.get(INPUT_VALUE)).get(
                        "prompts"
                    )
                    if prompts:
                        resolved_prompt = prompts[0]
                        output = json.loads(output)
                        output_text = (
                            output.get("generations")[0][0].get("text").strip()
                        )
                        extra_info = output.get("llm_output") or {}
                        model_id = extra_info.get("model_id")
                        token_usage = extra_info.get("token_usage")
                        generated_token_count = token_usage.get(
                            "generated_token_count"
                        )
                        input_token_count = token_usage.get(
                            "input_token_count"
                        )
                        metadata.update(
                            {
                                "model_id": model_id,
                                "generated_token_count": generated_token_count,
                                "input_token_count": input_token_count,
                            }
                        )

                        self._tracer.log_query_event(
                            query=str(resolved_prompt),  # type: ignore
                            # TODO: Scan for the system prompt in the input messages
                            # system_prompt=...
                            response=output_text,
                            span=span,
                            metadata=metadata,
                        )

                elif isinstance(output, str):
                    # If the output is a string, then it's answering a prompt/command

                    # Check if a template exists and resolve if it does
                    template: Optional[str] = span_attributes.get(
                        LLM_PROMPT_TEMPLATE
                    )
                    if template is not None:
                        # Get the user query from prompt template
                        template_variables = span_attributes[
                            LLM_PROMPT_TEMPLATE_VARIABLES
                        ]
                        if isinstance(template_variables, str):
                            template_variables = json.loads(template_variables)

                        resolved_prompt = template
                        for key, value in template_variables.items():
                            key_with_brackets = f"{{{key}}}"
                            resolved_prompt = resolved_prompt.replace(
                                key_with_brackets,
                                value,
                            )
                        metadata.update(
                            {
                                refine_metadata_key(
                                    LLM_PROMPT_TEMPLATE
                                ): template,
                                refine_metadata_key(
                                    LLM_PROMPT_TEMPLATE_VARIABLES
                                ): template_variables,
                            }
                        )
                    else:
                        # Get the user query from last user message

                        # message contains as key the index of the message
                        # and value the message info
                        # Example: {
                        #   0: {'content': 'What is (121 * 3)', 'role': 'user'},
                        #   1: {'arguments': {'a': 121, 'b': 3}, 'name': 'multiply'},
                        #   2: {'content': 363, 'name': 'multiply', 'role': 'tool'},
                        # }
                        input_messages: defaultdict[
                            int, dict[str, Union[str, dict[str, Any]]]
                        ] = defaultdict(dict)
                        for key, value in span_attributes.items():
                            if LLM_INPUT_MESSAGES in key:
                                # Example of key would be "llm.input_messages.0.message.role"
                                key_parts = key.split(".")
                                text_index: int = -1
                                for part in key_parts:
                                    if part.isnumeric():
                                        text_index = int(part)
                                if text_index == -1:
                                    continue

                                info_type = key.split(".")[-1]
                                input_messages[text_index][info_type] = value

                        # Find the most recent user message
                        for key, message in dict(
                            sorted(input_messages.items(), reverse=True)
                        ).items():
                            role = message.get("role")
                            if role is None or role != "user":
                                continue
                            resolved_prompt = message.get("content")

                    if "OpenAI" in span._name:
                        output = json.loads(output)
                        output_text = (
                            output.get("generations")[0][0].get("text").strip()
                        )
                        self._tracer.log_query_event(
                            query=str(resolved_prompt),  # type: ignore
                            # TODO: Scan for the system prompt in the input messages
                            # system_prompt=...
                            response=output_text,
                            span=span,
                            metadata=metadata,
                        )
                    else:
                        self._tracer.log_query_event(
                            query=str(resolved_prompt),  # type: ignore
                            # TODO: Scan for the system prompt in the input messages
                            # system_prompt=...
                            response=output,
                            span=span,
                            metadata=metadata,
                        )
                else:
                    # TODO: Support tool calls
                    pass
            elif "chain" == span_kind:
                self._tracer.log_synthesize_event(
                    input=span_attributes.get(INPUT_VALUE),
                    output=span_attributes.get(OUTPUT_VALUE),
                    span=span,
                )
            elif "parser" == span_kind:
                self._tracer.log_template_event(
                    prompt_template=span_attributes.get(INPUT_VALUE),
                    resolved_prompt=span_attributes.get(OUTPUT_VALUE),
                    span=span,
                )
            else:
                # Try to get input and output value from serialized payload
                input_value = serializable_payload.get(INPUT_VALUE)
                if input_value:
                    del serializable_payload[INPUT_VALUE]
                output_value = serializable_payload.get(OUTPUT_VALUE)
                if output_value:
                    del serializable_payload[OUTPUT_VALUE]

                # Pop off unnecessary keys
                serializable_payload.pop("openinference.span.kind", None)

                self._tracer.log_span_event(
                    input=input_value,
                    output=output_value,
                    name=span_kind,
                    span=span,
                    event_data=serializable_payload,
                    # event_kind=span_kind,
                )

        # n.b. we can't use real time because the handler may be called in a background thread.
        end_time_utc_nano = (
            _as_utc_nano(run.end_time) if run.end_time else None
        )

        span.end(end_time=end_time_utc_nano)


def _should_process(event_type: str) -> bool:
    """
    The LangChain event types are:
        1. "tool"
        2. "retriever"
        3. "chat_model"
        4. "llm"
        5. "chain"
        6. "parser"
        7. "prompt"

    Source: https://github.com/search?q=repo%3Alangchain-ai%2Flangchain+run_type%3D+language%3APython&type=code
    """

    SUPPORTED_EVENT_TYPES = set(
        ["tool", "retriever", "chat_model", "llm", "parser", "prompt", "chain"]
    )

    return event_type in SUPPORTED_EVENT_TYPES


# TODO(b7r6): this seems a bit ad-hoc and error-prone, figure out if we can wire into
# non-private APIs on `OpenInferenceTracer` and avoid this...
# https://github.com/langchain-ai/langchain/blob/5c2538b9f7fb64afed2a918b621d9d8681c7ae32/libs/core/langchain_core/callbacks/manager.py#L1876  # noqa: E501
class _BaseCallbackManagerInit:
    __slots__ = ("_tracer", "_cls")

    def __init__(
        self, tracer: LastMileTracer, cls: Type[_LastMileLangChainTracer]
    ):
        self._tracer = tracer
        self._cls = cls

    def __call__(
        self,
        wrapped: Callable[..., None],
        instance: BaseCallbackManager,
        args: Any,
        kwargs: Any,
    ) -> None:
        wrapped(*args, **kwargs)

        for handler in instance.inheritable_handlers:
            # n.b handlers may be copied when new managers are created, so we
            # don't want to keep adding. E.g. see the following location.
            if isinstance(handler, self._cls):
                break
        else:
            instance.add_handler(self._cls(tracer=self._tracer), True)
