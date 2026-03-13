"""
Task parsing utilities for IdeaSmith.

MVP behavior:
- Convert a plain-language idea into a list of actionable task strings.
- Keep it deterministic and easy to extend later with real LLM-backed parsing.
"""

from __future__ import annotations

from typing import List


def parse_tasks(idea_text: str) -> List[str]:
    """
    Convert an idea (plain text) into a list of task strings.

    Strategy (MVP):
    - If the user provided multiple lines, treat each non-empty line as a task.
    - Otherwise, split on common sentence delimiters and create tasks from clauses.

    Args:
        idea_text: Free-form user idea text.

    Returns:
        A list of tasks (strings). Never returns an empty list; falls back to one task.
    """
    text = (idea_text or "").strip()
    if not text:
        return ["Clarify project idea (no input provided)."]

    # Prefer line-based tasks if the user enters multiple lines / bullets.
    lines = [ln.strip(" \t-•") for ln in text.splitlines()]
    tasks = [ln for ln in lines if ln]
    if len(tasks) >= 2:
        return tasks

    # Sentence-ish splitting for single-paragraph ideas.
    # Keep it simple for MVP (no heavy NLP).
    for delim in [".", ";", " and ", " then "]:
        if delim.strip() in text:
            parts = [p.strip(" \t-•.,;") for p in text.replace("\n", " ").split(delim)]
            tasks = [p for p in parts if p]
            break

    if not tasks:
        tasks = [text]

    # Make tasks feel like tasks (optional light normalization).
    normalized: List[str] = []
    for t in tasks:
        t = t.strip()
        if not t:
            continue
        # If it doesn't look imperative, prefix with "Do:" for clarity.
        if not t.lower().startswith(("build", "create", "implement", "design", "add", "write", "set up", "setup")):
            t = f"Do: {t}"
        normalized.append(t)

    return normalized or [text]

