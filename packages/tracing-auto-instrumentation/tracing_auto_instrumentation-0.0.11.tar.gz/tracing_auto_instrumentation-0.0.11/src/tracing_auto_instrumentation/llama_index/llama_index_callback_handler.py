import json
import logging
from collections import defaultdict
from time import time_ns
from typing import Any, Dict, Optional, Union

from lastmile_eval.rag.debugger.api import (
    LastMileTracer,
    RetrievedChunk,
    TextEmbedding,
)
from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer
from llama_index.core.callbacks import CBEventType, EventPayload
from openinference.instrumentation.llama_index._callback import (
    OpenInferenceTraceCallbackHandler,
    payload_to_semantic_attributes,
    _is_streaming_response,  # type: ignore
    _flatten,  # type: ignore
    _ResponseGen,  # type: ignore
    _EventData,  # type: ignore
    # Opinionated params we explicit want to save, see source for full list
    EMBEDDING_EMBEDDINGS,
    EMBEDDING_MODEL_NAME,
    INPUT_VALUE,
    LLM_INVOCATION_PARAMETERS,
    LLM_MODEL_NAME,
    LLM_INPUT_MESSAGES,
    LLM_PROMPT_TEMPLATE,
    LLM_PROMPT_TEMPLATE_VARIABLES,
    LLM_TOKEN_COUNT_COMPLETION,
    LLM_TOKEN_COUNT_PROMPT,
    LLM_TOKEN_COUNT_TOTAL,
    OUTPUT_VALUE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_K,
    RETRIEVAL_DOCUMENTS,
    # # Explicit chose not to do this because we can extract it from OUTPUT_VALUE
    # LLM_OUTPUT_MESSAGES,
)
from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.context import _SUPPRESS_INSTRUMENTATION_KEY  # type: ignore
from opentelemetry.sdk.trace import ReadableSpan

from ..utils import DEFAULT_TRACER_NAME_PREFIX

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# In general, only store "configuration" params instead of values that can
# dynamically change at run-time for each rag event like input messages

# We are choosing not to save any params in auto-instrumentation for
# event callback/handler instrumentors
# The reason why wrappers can save params is that the wrapper calls
# the underlying LLM API once, so we only save params once, whereas
# the event callbacks get called for every single event type within
# llama index or langchain, so they can be called multiple times and
# cause param set to be spammy
EVENT_DATA_KEY_SUBSTRING_MATCHES = (
    EMBEDDING_MODEL_NAME,
    INPUT_VALUE,
    LLM_INVOCATION_PARAMETERS,
    LLM_MODEL_NAME,
    LLM_PROMPT_TEMPLATE,
    LLM_TOKEN_COUNT_TOTAL,
    OUTPUT_VALUE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_K,
)


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


class LlamaIndexCallbackHandler(OpenInferenceTraceCallbackHandler):
    """
    This is a callback handler for automatically instrumenting with
    LLamaIndex. Here's how to use it:

    ```
    from lastmile_eval.rag.debugger.tracing import LlamaIndexCallbackHandler
    llama_index.core.global_handler = LlamaIndexCallbackHandler()
    # Do regular LlamaIndex calls as usual
    ```
    """

    def __init__(
        self,
        project_name: Optional[str] = None,
        lastmile_api_token: Optional[str] = None,
    ):
        project_name = project_name or (
            DEFAULT_TRACER_NAME_PREFIX + " - LlamaIndex"
        )
        tracer = get_lastmile_tracer(
            tracer_name=project_name,
            project_name=project_name,
            lastmile_api_token=lastmile_api_token,
        )
        super().__init__(tracer)

    def get_tracer(self) -> LastMileTracer:
        return self._tracer

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
            return

        with self._lock:
            if event_type is CBEventType.TEMPLATING:
                if (
                    parent_id := self._templating_parent_id.pop(event_id, None)
                ) and payload:
                    if parent_id in self._templating_payloads:
                        self._templating_payloads[parent_id].append(payload)
                    else:
                        self._templating_payloads[parent_id] = [payload]
                return
            if not (event_data := self._event_data.pop(event_id, None)):
                return

        event_data.end_time = time_ns()
        is_dispatched = False

        if payload is not None:
            event_data.payloads.append(payload.copy())
            if isinstance(
                (exception := payload.get(EventPayload.EXCEPTION)), Exception
            ):
                event_data.exceptions.append(exception)
            try:
                event_data.attributes.update(
                    payload_to_semantic_attributes(
                        event_type, payload, is_event_end=True
                    ),
                )
            except Exception:
                logger.exception(
                    f"Failed to convert payload to semantic attributes. "
                    f"event_type={event_type}, payload={payload}",
                )
            if (
                _is_streaming_response(
                    response := payload.get(EventPayload.RESPONSE)
                )
                and response.response_gen is not None
            ):
                response.response_gen = _ResponseGen(
                    response.response_gen, event_data
                )
                is_dispatched = True

        if not is_dispatched:
            _finish_tracing(
                event_data,
                tracer=self._tracer,
                event_type=event_type,
            )
        return


def _finish_tracing(
    event_data: _EventData,
    tracer: LastMileTracer,
    event_type: CBEventType,
) -> None:
    if not (span := event_data.span):
        return
    attributes = event_data.attributes
    if event_data.exceptions:
        status_descriptions: list[str] = []
        for exception in event_data.exceptions:
            span.record_exception(exception)
            # Follow the format in OTEL SDK for description, see:
            # https://github.com/open-telemetry/opentelemetry-python/blob/2b9dcfc5d853d1c10176937a6bcaade54cda1a31/opentelemetry-api/src/opentelemetry/trace/__init__.py#L588  # noqa E501
            status_descriptions.append(
                f"{type(exception).__name__}: {exception}"
            )
        status = trace_api.Status(
            status_code=trace_api.StatusCode.ERROR,
            description="\n".join(status_descriptions),
        )
    else:
        status = trace_api.Status(status_code=trace_api.StatusCode.OK)
    span.set_status(status=status)
    try:
        span.set_attributes(dict(_flatten(attributes)))

        # Remove "serialized" from the spans
        # We need to do this because this info stores the API keys and we
        # want to remove. Other pertinent data is stored in the span attributes
        # like model name and invocation params already
        if (
            isinstance(span, ReadableSpan)
            and span._attributes is not None
            and "serialized" in span._attributes
        ):
            del span._attributes["serialized"]

        if not _should_skip(event_type):
            span_attributes: dict[str, Any] = span._attributes  # type: ignore
            event_payload: dict[str, Any] = {}
            for key, value in span._attributes.items():
                # Only save the opinionated data to event data and param set
                if _save_to_event_data(key):
                    event_payload[refine_metadata_key(key)] = value

            event_type = event_data.event_type
            if event_type == CBEventType.QUERY:
                tracer.log_query_event(
                    query=span_attributes[INPUT_VALUE],
                    response=span_attributes[OUTPUT_VALUE],
                    span=span,
                )
            elif event_type == CBEventType.RETRIEVE:
                # extract document data

                # doc_info contains as key the index of the document and value the
                # info of the document
                # Example: {0: {'id': 'doc1', 'score': 0.5, 'content': 'doc1 content'}}
                doc_info: defaultdict[int, dict[str, Union[str, float]]] = (
                    defaultdict(dict)
                )
                for key, value in span_attributes.items():
                    if RETRIEVAL_DOCUMENTS in key:
                        # Example of key would be "retrieval.documents.1.document.score"
                        key_parts = key.split(".")
                        doc_index: int = -1
                        for part in key_parts:
                            if part.isnumeric():
                                doc_index = int(part)
                        if doc_index == -1:
                            continue

                        # info will be either "id", "score", or "content"
                        info_type = key.split(".")[-1]
                        doc_info[doc_index][info_type] = value

                # build list of retrieved nodes
                retrieved_chunks: list[RetrievedChunk] = []
                # Sort the keys (document index) to add them in correct order
                # to the retrieved nodes array
                for info_dict in dict(sorted(doc_info.items())).values():
                    retrieved_chunks.append(
                        RetrievedChunk(
                            id=str(info_dict["id"]),
                            retrieval_score=float(info_dict["score"]),
                            content=str(info_dict["content"]),
                        )
                    )
                tracer.log_retrieval_event(
                    query=span_attributes[INPUT_VALUE],
                    retrieved_data=retrieved_chunks,
                    span=span,
                )
            elif event_type == CBEventType.EMBEDDING:
                # embed_info contains as key the index of the text chunk
                # (or query) and value the embedding info
                # Example: {0: {'text': 'something to embed', 'vector': [0.1, 0.2, 0.3 ... 0.2343]}}
                embed_info: defaultdict[
                    int, dict[str, Union[str, list[float]]]
                ] = defaultdict(dict)
                model_name: str = ""
                for key, value in span_attributes.items():
                    if EMBEDDING_EMBEDDINGS in key:
                        # Example of key would be "embedding.embeddings.0.embedding.text"
                        key_parts = key.split(".")
                        text_index: int = -1
                        for part in key_parts:
                            if part.isnumeric():
                                text_index = int(part)
                        if text_index == -1:
                            continue

                        # info will be either "text", or "vector"
                        info_type = key.split(".")[-1]
                        embed_info[text_index][info_type] = value
                    if EMBEDDING_MODEL_NAME in key:
                        model_name = value

                # build list of embeddings
                embeddings: list[TextEmbedding] = []
                for key, info_dict in dict(sorted(embed_info.items())).items():
                    embeddings.append(
                        TextEmbedding(
                            id=f"embedding-{key}",
                            text=str(info_dict["text"]),
                            vector=list(info_dict["vector"]),  # type: ignore
                        )
                    )

                if len(embeddings) == 1:
                    tracer.log_embedding_event(
                        embeddings=embeddings,
                        span=span,
                        metadata={
                            f"{refine_metadata_key(EMBEDDING_MODEL_NAME)}": model_name,
                        },
                    )
                elif len(embeddings) > 1:
                    curr_span_index: str = span._name[0]
                    span.update_name(f"{curr_span_index} - multi_embedding")
                    tracer.log_embedding_event(
                        embeddings=embeddings,
                        span=span,
                        metadata={
                            "embedding_count": len(embed_info),
                            f"{refine_metadata_key(EMBEDDING_MODEL_NAME)}": model_name,
                        },
                    )
            elif event_type == CBEventType.LLM:
                output = span_attributes[OUTPUT_VALUE]
                if isinstance(output, str):
                    # If the output is a string, then it's answering a prompt/command
                    metadata = {
                        refine_metadata_key(
                            LLM_TOKEN_COUNT_COMPLETION
                        ): span_attributes[LLM_TOKEN_COUNT_COMPLETION],
                        refine_metadata_key(
                            LLM_TOKEN_COUNT_PROMPT
                        ): span_attributes[LLM_TOKEN_COUNT_PROMPT],
                        refine_metadata_key(
                            LLM_TOKEN_COUNT_TOTAL
                        ): span_attributes[LLM_TOKEN_COUNT_TOTAL],
                    }

                    # Un-nest completion params from llm.invocation_parameters
                    completion_params = span_attributes.get(
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

                    # Check if a template exists and resolve if it does
                    # TODO: Shouldn't this instead be a child span template event?
                    template: Optional[str] = span_attributes.get(
                        LLM_PROMPT_TEMPLATE
                    )
                    resolved_prompt = None

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

                    tracer.log_query_event(
                        query=str(resolved_prompt),  # type: ignore
                        # TODO: Scan for the system prompt in the input messages
                        # system_prompt=...
                        response=span_attributes[OUTPUT_VALUE],
                        span=span,
                        metadata=metadata,
                    )
                else:
                    # TODO: Support tool calls
                    pass
            # elif event_type == CBEventType.FUNCTION_CALL:
            #     tracer.log_tool_call_event(span_attributes[TOOL_NAME])
            else:
                span_kind = str(event_data.event_type.value)
                tracer.log_span_event(
                    name=span_kind,
                    span=span,
                    event_data=event_payload,
                    # TODO (rossdan): Add mapping between span_kind and RAGEventType
                    # event_kind=span_kind,
                )

    except Exception:
        logger.exception(
            f"Failed to set attributes on span. event_type={event_data.event_type}, "
            f"attributes={attributes}",
        )
    span.end(end_time=event_data.end_time)


def _should_skip(event_type: CBEventType) -> bool:
    # TODO: Add some actual crieria for skipping to log span events
    return event_type in {
        CBEventType.CHUNKING,
        CBEventType.NODE_PARSING,
        CBEventType.TREE,
        CBEventType.SYNTHESIZE,
    }


def _save_to_event_data(key: str):
    for substring in EVENT_DATA_KEY_SUBSTRING_MATCHES:
        if substring in key:
            return True
    return False


# TODO: Clean later, for now it's just helpful for me to keep track of all events
def _add_rag_event_to_tracer() -> None:
    """
    Skip these
    CHUNKING = "chunking"
    NODE_PARSING = "node_parsing"
    SYNTHESIZE = "synthesize"
    TREE = "tree"

    Done
    QUERY = "query"
    RETRIEVE = "retrieve"
    EMBEDDING = "embedding"
    LLM = "llm" # part of query
    FUNCTION_CALL = "function_call"

    TODO
    SUB_QUESTION = "sub_question"
    TEMPLATING = "templating"
    RERANKING = "reranking"
    EXCEPTION = "exception"
    AGENT_STEP = "agent_step"
    """
