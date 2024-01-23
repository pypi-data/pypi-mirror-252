from typing import Optional

from prometheus_client import Histogram

from cashews import cache
from cashews._typing import Middleware
from cashews.backends.interface import Backend
from cashews.commands import Command


def create_metrics_middleware(latency_metric: Optional[Histogram] = None, with_tag: bool = False) -> Middleware:
    _DEFAULT_METRIC = Histogram(
        "cashews_operations_latency_seconds",
        "Latency of different operations with a cache",
        labelnames=["operation", "backend_class"] if not with_tag else ["operation", "backend_class", "tag"],
    )
    _latency_metric = latency_metric or _DEFAULT_METRIC

    async def metrics_middleware(call, cmd: Command, backend: Backend, *args, **kwargs):
        with _latency_metric.time() as metric:
            metric.labels(operation=cmd.value, backend_class=backend.__class__.__name__)
            if with_tag and "key" in kwargs:
                tags = cache.get_key_tags(kwargs["key"])
                tag = next((t for t in tags), None)
                if tag:
                    metric.labels(tag=tag)
            return await call(*args, **kwargs)

    return metrics_middleware
