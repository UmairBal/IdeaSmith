"""
Task execution utilities for IdeaSmith.

MVP behavior:
- Do not perform real side effects.
- Return a deterministic string confirming completion.
"""

from __future__ import annotations


def execute_task(task: str) -> str:
    """
    Execute a task and return its output.

    Args:
        task: A task description string.

    Returns:
        A simple completion message (MVP).
    """
    task = (task or "").strip()
    if not task:
        return "Completed: (empty task)"
    return f"Completed: {task}"

