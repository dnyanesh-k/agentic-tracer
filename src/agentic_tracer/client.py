from storage import FileStorage
from typing import Optional

class TracerClient:
    """Client for tracing agent execution.
    Routes trace operations based on mode. Currently supports local file storage; API mode is placeholder.
    Attributes:
        mode: Storage backend to use ("file" or "api").
        storage: FileStorage instance if mode is "file" else None.
    """

    def __init__(
        self,
        mode: str = "file",
        storage_dir: str = "./traces"
    ):
        """
            Args:
                mode: Storage backend to use ("file" or "api"). Defaults to "file".
                storage_dir: Directory for trace files, used only when mode is "file". Defaults to "./traces".
        """
        self.mode = mode
        self.storage = FileStorage(storage_dir) if mode == "file" else None

    def start_trace(
            self,
            input_text: str,
            project_id: int = 1
    ) -> int:
        """Begins a new trace.
        
        Args:
            input_text: The user's input that starts the trace.
            project_id: Unique identifier of the project this trace belongs to. Defaults to 1.
        
        Returns:
            The generated trace ID, or 0 in API mode (placeholder).
        """
        if self.mode == "file":
            self.storage.start_trace(input_text, project_id)
        return 0

    def add_step(
            self,
            trace_id: int,
            step_type: str,
            content: dict,
            latency_ms: int = 0
    ):
        """Appends a step to given trace.
        
        Args:
            trace_id: ID of trace to append to.
            step_type: Category of step (e.g. "tool_call", "llm_call").
            content: Data associated with the step.
            latency_ms: Time taken to execute the step, in milliseconds. Defaults to 0.
        """
        if self.mode == "file":
            self.storage.add_step(step_type, content, latency_ms)

    def complete_trace(
            self,
            trace_id: int,
            final_output: str,
            success: bool = True
    ) -> Optional[dict]:
        """Finalizes the given trace.
        
        Args:
            trace_id: ID of the trace to complete.
            final_output: The agent's final output.
            success: Whether the execution completed successfully. Defaults to True.
        
        Returns:
            The completed trace dict in file mode, else None.
        """
        if self.mode == "file":
            return self.storage.complete_trace(final_output, success)
        