from typing import Dict, List, Any, Optional

class TraceStep:
    """Represents an individual step in agent execution.
    
    Args:
        step_type: Category of step (e.g. "tool_call", "llm_call").
        content: Data associated with the step.
        latency_ms: Time taken to execute the step, in milliseconds.
            Defaults to 0.
    """

    def __init__(
        self, 
        step_type: str, 
        content: Dict, 
        latency_ms: int = 0
    ):
        self.step_type = step_type
        self.content = content
        self.latency_ms = latency_ms


class Trace:
    """
    Represent one complete agent execution.

    Attributes:
        trace_id: Unique identifier for this trace.
        input_txt: The original user input.
        steps: Ordered list of steps taken by the agent.
        final_output: The agent's final output, if completed.
        success: Weather the execution completed successfully.

    Args:
        trace_id: Unique identifier for this trace.
        input_txt: The original user input.
    """

    def __init__(
        self, 
        trace_id: int, 
        input_txt: str
    ):
        self.trace_id = trace_id
        self.input_txt = input_txt
        self.steps : List[TraceStep] = []
        self.final_output = ""
        self.success = True