"""
Some utils used by the dogtrace redis integration
"""
from contextlib import contextmanager
from typing import List
from typing import Optional

from ddtrace.constants import ANALYTICS_SAMPLE_RATE_KEY
from ddtrace.constants import SPAN_KIND
from ddtrace.constants import SPAN_MEASURED_KEY
from ddtrace.contrib import trace_utils
from ddtrace.contrib.redis_utils import _extract_conn_tags
from ddtrace.ext import SpanKind
from ddtrace.ext import SpanTypes
from ddtrace.ext import db
from ddtrace.ext import redis as redisx
from ddtrace.internal import core
from ddtrace.internal.constants import COMPONENT
from ddtrace.internal.schema import schematize_cache_operation
from ddtrace.internal.utils.formats import stringify_cache_args


format_command_args = stringify_cache_args


def _set_span_tags(
    span, pin, config_integration, args: Optional[List], instance, query: Optional[List], is_cluster: bool = False
):
    span.set_tag_str(SPAN_KIND, SpanKind.CLIENT)
    span.set_tag_str(COMPONENT, config_integration.integration_name)
    span.set_tag_str(db.SYSTEM, redisx.APP)
    span.set_tag(SPAN_MEASURED_KEY)
    if query is not None:
        span_name = schematize_cache_operation(redisx.RAWCMD, cache_provider=redisx.APP)  # type: ignore[operator]
        span.set_tag_str(span_name, query)
    if pin.tags:
        span.set_tags(pin.tags)
    # some redis clients do not have a connection_pool attribute (ex. aioredis v1.3)
    if not is_cluster and hasattr(instance, "connection_pool"):
        span.set_tags(_extract_conn_tags(instance.connection_pool.connection_kwargs))
    if args is not None:
        span.set_metric(redisx.ARGS_LEN, len(args))
    else:
        for attr in ("command_stack", "_command_stack"):
            if hasattr(instance, attr):
                span.set_metric(redisx.PIPELINE_LEN, len(getattr(instance, attr)))
    # set analytics sample rate if enabled
    span.set_tag(ANALYTICS_SAMPLE_RATE_KEY, config_integration.get_analytics_sample_rate())


@contextmanager
def _instrument_redis_cmd(pin, config_integration, instance, args):
    query = stringify_cache_args(args, cmd_max_len=config_integration.cmd_max_length)
    with core.context_with_data(
        "redis.command",
        span_name=schematize_cache_operation(redisx.CMD, cache_provider=redisx.APP),
        pin=pin,
        service=trace_utils.ext_service(pin, config_integration),
        span_type=SpanTypes.REDIS,
        resource=query.split(" ")[0] if config_integration.resource_only_command else query,
        call_key="redis_command_call",
    ) as ctx, ctx[ctx["call_key"]] as span:
        _set_span_tags(span, pin, config_integration, args, instance, query)
        yield ctx


@contextmanager
def _instrument_redis_execute_pipeline(pin, config_integration, cmds, instance, is_cluster=False):
    cmd_string = resource = "\n".join(cmds)
    if config_integration.resource_only_command:
        resource = "\n".join([cmd.split(" ")[0] for cmd in cmds])

    with pin.tracer.trace(
        schematize_cache_operation(redisx.CMD, cache_provider=redisx.APP),
        resource=resource,
        service=trace_utils.ext_service(pin, config_integration),
        span_type=SpanTypes.REDIS,
    ) as span:
        _set_span_tags(span, pin, config_integration, None, instance, cmd_string)
        yield span


@contextmanager
def _instrument_redis_execute_async_cluster_pipeline(pin, config_integration, cmds, instance):
    cmd_string = resource = "\n".join(cmds)
    if config_integration.resource_only_command:
        resource = "\n".join([cmd.split(" ")[0] for cmd in cmds])

    with pin.tracer.trace(
        schematize_cache_operation(redisx.CMD, cache_provider=redisx.APP),
        resource=resource,
        service=trace_utils.ext_service(pin, config_integration),
        span_type=SpanTypes.REDIS,
    ) as span:
        _set_span_tags(span, pin, config_integration, None, instance, cmd_string)
        yield span
