"""
Manager AI for IdeaSmith.

Responsibilities (MVP):
- Receive a user's idea
- Convert it into tasks (using task_parser.parse_tasks)
- Review Developer outputs and approve/reject (MVP: approve everything)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from manager_ai.task_parser import parse_tasks


@dataclass(frozen=True)
class ReviewResult:
    """Represents the Manager's review decision for a given task output."""

    approved: bool
    feedback: str = ""


class ManagerAI:
    """
    A simple supervising agent.

    This class is intentionally lightweight so you can replace its logic with real
    AI calls later.
    """

    def __init__(self, name: str = "ManagerAI") -> None:
        self.name = name

    def create_tasks(self, idea_text: str) -> List[str]:
        """
        Create a list of tasks from the user idea.
        """
        return parse_tasks(idea_text)

    def review_output(self, task: str, developer_output: str) -> ReviewResult:
        """
        Review a DeveloperAI output.

        MVP policy:
        - Always approve.
        - Provide a short acknowledgement as feedback.
        """
        _ = task  # reserved for richer review logic later
        _ = developer_output
        return ReviewResult(approved=True, feedback="Approved (MVP policy).")

