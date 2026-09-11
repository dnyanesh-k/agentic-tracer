from functools import wraps
import time
from typing import Callable
from .client import TracerClient

def trace(client: TracerClient):
    """Decorator factory wraps an async function to record it as trace.
    
    Captures the function's input, starts a trace before execution and records completion (or failure) after execution.
    
    Args:
        client: TracerClient instace used to record the trace.
    
    Returns:
        A decorator that wraps async functions with tracing.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # extract input 
            input_text = str(kwargs.get("input", args[0] if args else ""))
            latency_ms = int((time.time() - start_time) * 1000)
            start_time = time.time()
            # start trace
            trace_id = client.start_trace(input_text)
            

            # create a step adder
            async def add_step(
                    step_type: str,
                    content: dict,
                    latency_ms: int
            ):
                client.add_step(trace_id, step_type, content, latency_ms)

            try:
                # execute the agent with trace context and passes these 3 thiongs args
                result = await func(*args, **kwargs, _trace_add_step=add_step)

                
                client.complete_trace(
                    trace_id, 
                    str(result),
                    True
                )
                return result
            except Exception as e:
                client.complete_trace(
                    trace_id, 
                    str(e),
                    False
                )
                raise
            
        return wrapper
    return decorator

