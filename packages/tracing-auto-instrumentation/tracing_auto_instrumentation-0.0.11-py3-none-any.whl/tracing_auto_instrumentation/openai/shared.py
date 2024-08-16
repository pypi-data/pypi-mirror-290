# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import Any, Mapping, Optional, ParamSpecKwargs

from lastmile_eval.rag.debugger.api import LastMileTracer
from opentelemetry.trace import Span

from ..utils import json_serialize_anything, T_co


def parse_params(params: dict[str, ParamSpecKwargs]):
    # First, destructively remove span_info
    empty_dict: dict[str, Any] = {}
    ret = params.pop("span_info", empty_dict)

    # Then, copy the rest of the params
    params = {**params}
    messages = params.pop("messages", None)
    return _merge_dicts(
        ret,
        {
            "input": messages,
            "metadata": params,
        },
    )


def _merge_dicts(d1: dict[T_co, Any], d2: dict[T_co, Any]) -> dict[T_co, Any]:
    return {**d1, **d2}


def flatten_json(obj: Mapping[str, Any]):
    return {k: json_serialize_anything(v) for k, v in obj.items()}


def add_rag_event_with_output(
    tracer: LastMileTracer,
    event_name: str,
    span: Optional[Span] = None,  # type: ignore
    input: Optional[Any] = None,
    output: Optional[Any] = None,
    event_data: dict[Any, Any] | None = None,
    span_kind: Optional[str] = None,
) -> None:
    if output is not None:
        # TODO (rossdan): Fill in system prompt
        tracer.log_query_event(
            query=str(input),
            response=output,
            span=span,
            metadata=event_data,
        )
    else:
        tracer.log_span_event(
            name=event_name,
            event_data=event_data,
            span=span,
            event_kind=span_kind,
        )
