from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from ddtrace import Span
from ddtrace import config
from ddtrace.constants import ANALYTICS_SAMPLE_RATE_KEY
from ddtrace.constants import SPAN_KIND
from ddtrace.constants import SPAN_MEASURED_KEY
from ddtrace.ext import SpanKind
from ddtrace.ext import aws
from ddtrace.ext import http
from ddtrace.internal.constants import COMPONENT
from ddtrace.internal.utils.formats import deep_getattr
from ddtrace.propagation.http import HTTPPropagator


def set_botocore_patched_api_call_span_tags(span: Span, instance, args, params, endpoint_name, operation):
    span.set_tag_str(COMPONENT, config.botocore.integration_name)
    # set span.kind to the type of request being performed
    span.set_tag_str(SPAN_KIND, SpanKind.CLIENT)
    span.set_tag(SPAN_MEASURED_KEY)

    if args:
        # DEV: join is the fastest way of concatenating strings that is compatible
        # across Python versions (see
        # https://stackoverflow.com/questions/1316887/what-is-the-most-efficient-string-concatenation-method-in-python)
        span.resource = ".".join((endpoint_name, operation.lower()))
        span.set_tag("aws_service", endpoint_name)

        if params and not config.botocore["tag_no_params"]:
            aws._add_api_param_span_tags(span, endpoint_name, params)

    else:
        span.resource = endpoint_name

    region_name = deep_getattr(instance, "meta.region_name")

    span.set_tag_str("aws.agent", "botocore")
    if operation is not None:
        span.set_tag_str("aws.operation", operation)
    if region_name is not None:
        span.set_tag_str("aws.region", region_name)
        span.set_tag_str("region", region_name)

    # set analytics sample rate
    span.set_tag(ANALYTICS_SAMPLE_RATE_KEY, config.botocore.get_analytics_sample_rate())


def set_botocore_response_metadata_tags(
    span: Span, result: Dict[str, Any], is_error_code_fn: Optional[Callable] = None
) -> None:
    if not result or not result.get("ResponseMetadata"):
        return
    response_meta = result["ResponseMetadata"]

    if "HTTPStatusCode" in response_meta:
        status_code = response_meta["HTTPStatusCode"]
        span.set_tag(http.STATUS_CODE, status_code)

        # Mark this span as an error if requested
        if is_error_code_fn is not None and is_error_code_fn(int(status_code)):
            span.error = 1

    if "RetryAttempts" in response_meta:
        span.set_tag("retry_attempts", response_meta["RetryAttempts"])

    if "RequestId" in response_meta:
        span.set_tag_str("aws.requestid", response_meta["RequestId"])


def extract_DD_context_from_messages(messages, extract_from_message: Callable):
    ctx = None
    if len(messages) >= 1:
        message = messages[0]
        context_json = extract_from_message(message)
        if context_json is not None:
            child_of = HTTPPropagator.extract(context_json)
            if child_of.trace_id is not None:
                ctx = child_of
    return ctx
