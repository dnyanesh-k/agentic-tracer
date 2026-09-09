class LangGraphTracer:
    def __init__(self, client):
        self.client = client
    
    def instrument(self, graph):
        original = graph.step
        async def traced_step(state, *args, **kwargs):
            trace_id = self.client.start_trace(str(state))
            result = await original(state, *args, **kwargs)
            self.client.add_step(trace_id, "step", {"result": str(result)})
            self.client.complete_trace(trace_id, str(result))
            return result
        graph.step = traced_step
        return graph