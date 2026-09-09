import asyncio
from agentic_tracer import TracerClient, trace

tracer = TracerClient(mode="file", storage_dir="./traces")

@trace(tracer)
async def my_agent(input_text: str, **kwargs) -> str:
    # Get the step adder from kwargs
    _trace_add_step = kwargs.get("_trace_add_step")
    
    if _trace_add_step:
        await _trace_add_step("thought", {"reasoning": f"Processing: {input_text}"})
    
    result = f"Processed: {input_text}"
    
    if _trace_add_step:
        await _trace_add_step("final_answer", {"answer": result})
    
    return result

async def main():
    result = await my_agent("Hello World")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())