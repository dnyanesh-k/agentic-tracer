from contextlib import asynccontextmanager

@asynccontextmanager
async def trace_context(client, input_text: str):
    trace_id = client.start_trace(input_text)
    step_counter = 0
    
    class Ctx:
        async def thought(self, reasoning: str):
            nonlocal step_counter
            step_counter += 1
            client.add_step(trace_id, "thought", {"reasoning": reasoning})
        
        async def tool_call(self, tool: str, params: dict):
            nonlocal step_counter
            step_counter += 1
            client.add_step(trace_id, "tool_call", {"tool": tool, "params": params})
        
        async def observation(self, result: any):
            nonlocal step_counter
            step_counter += 1
            client.add_step(trace_id, "observation", {"result": result})
        
        async def final_answer(self, answer: str):
            nonlocal step_counter
            step_counter += 1
            client.add_step(trace_id, "final_answer", {"answer": answer})
            client.complete_trace(trace_id, answer, True)
    
    try:
        yield Ctx()
    except Exception as e:
        client.complete_trace(trace_id, str(e), False)
        raise