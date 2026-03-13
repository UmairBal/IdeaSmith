"""
IdeaSmith CLI (MVP).

Run:
    python interface/main.py

Flow:
- Read a user idea from stdin (supports multi-line input).
- ManagerAI converts idea -> tasks.
- DeveloperAI executes tasks.
- ManagerAI reviews outputs.
- Print a final report.
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple

# Allow running this file directly (`python interface/main.py`) from any CWD by
# ensuring the project root is on sys.path.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from developer_ai.developer import DeveloperAI
from manager_ai.manager import ManagerAI, ReviewResult


def _read_multiline_input(prompt: str) -> str:
    """
    Read multi-line text from the user until a blank line is entered.
    """
    print(prompt)
    print("(Enter a blank line to finish.)")
    lines: List[str] = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run_pipeline(idea_text: str) -> Tuple[List[str], List[str], List[ReviewResult]]:
    """
    Run the Manager->Developer->Manager loop for a given idea.

    Returns:
        tasks, outputs, reviews
    """
    manager = ManagerAI()
    developer = DeveloperAI()

    tasks = manager.create_tasks(idea_text)
    outputs = developer.execute(tasks)
    reviews = [manager.review_output(task, out) for task, out in zip(tasks, outputs)]
    return tasks, outputs, reviews


def main() -> None:
    idea_text = _read_multiline_input("Describe your project idea:")
    tasks, outputs, reviews = run_pipeline(idea_text)

    print("\n=== IdeaSmith Results (MVP) ===\n")
    for idx, (task, out, review) in enumerate(zip(tasks, outputs, reviews), start=1):
        status = "APPROVED" if review.approved else "REJECTED"
        print(f"Task {idx}: {task}")
        print(f"Output : {out}")
        print(f"Review : {status} - {review.feedback}")
        print("-" * 40)

    all_approved = all(r.approved for r in reviews)
    print("\nFinal decision:", "ALL APPROVED" if all_approved else "NEEDS REVISION")


if __name__ == "__main__":
    main()

