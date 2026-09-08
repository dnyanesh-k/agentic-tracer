import json
from pathlib import Path
from typing import Dict, Optional

class FileStorage:
    """Persists agents traces to disk as JSON files
    
    Stores one trace at a time in memory during execution, then writes it to a JSON file when the trace completes.

    Attributes:
        storage_dir: Directory where trace JSON files are saved.
    """

    def __init__(
        self,
        storage_dir: str = "./traces"
    ):
        """
        Args:
            storage_dir: Directory where trace JSON files are saved. Created when does not exist. Defaults to "./traces".
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._counter = 1

    def start_trace(
            self,
            input_text: str,
            project_id: int = 1
    ) -> int :
        """Begins a new trace and set it as current active trace.

        Args:
            input_text: The user's input that start this trace.
            project_id: Identifier of the project this trace belongs to.
                Defaults to 1.

        Returns:
            The generated trace ID.                
        """
        trace_id = self._counter
        self._counter += 1
        self._current_trace = {"id": trace_id, "input": input_text, "steps": []}
        return trace_id

    def add_step(
            self,
            step_type: str,
            content: dict,
            latency_ms: int = 0
    ):
        """Appends a step to currently active trace.
        
        Args:
            step_type: Category of step (e.g. "tool_call", "llm_call").
            content: Data associated with the step.
            latency_ms: Time taken to execute the step, im milliseconds.
                Defaults to 0.

        Raises:
            RuntimeError: If no trace is currently active.
        """
        if not hasattr(self, "_current_trace"):
            raise RuntimeError("No active trace.")
        
        self._current_trace["steps"].append({
            "step_type": step_type,
            "content": content,
            "latency_ms": latency_ms
        })

    def complete_trace(
            self,
            final_output: str,
            success: bool = True
    ) -> dict:
        """Finalizes the current trace and writes it to the disk.
        
        Args:
            final_output: The agent's finaloutput.
            success: Whether the execuction completed successfully.
                Defaults to True.
        
        Returns:
            The completed trace as dict.
        """
        if not hasattr(self, "_current_trace"):
            raise RuntimeError("No active trace.")

        self._current_trace["final_output"] = final_output
        self._current_trace["success"] = success
        trace_id = self._current_trace["id"]
        filename = self.storage_dir / f"trace_{trace_id}.json"

        with open(filename, "w") as f:
            json.dump(self._current_trace, f, indent=2)
            
        return self._current_trace