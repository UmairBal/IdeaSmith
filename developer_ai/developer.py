"""
Developer AI for IdeaSmith.

Responsibilities (MVP):
- Receive tasks from ManagerAI
- Execute tasks using executor.execute_task
- Return outputs back to the Manager
"""

from __future__ import annotations

from typing import List

from developer_ai.executor import execute_task


class DeveloperAI:
    """
    A minimal "worker" agent that executes tasks.
    """

    def __init__(self, name: str = "DeveloperAI") -> None:
        self.name = name

    def execute(self, tasks: List[str]) -> List[str]:
        """
        Execute a list of tasks and return outputs in the same order.
        """
        outputs: List[str] = []
        for task in tasks:
            outputs.append(execute_task(task))
        return outputs

