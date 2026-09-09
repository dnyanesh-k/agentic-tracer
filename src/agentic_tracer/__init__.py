from .client import TracerClient
from .decorators import trace
from .context import trace_context

__version__ = "0.1.0"

#  create tracer export
def create_tracer():
    """Create a tracer client with default settings."""
    return TracerClient(mode="file", storage_dir="./data/traces")

__version__ = "0.1.0"

__all__ = [
    "TracerClient",
    "trace",
    "trace_context",
    "create_tracer",
]