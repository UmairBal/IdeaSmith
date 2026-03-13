import json
from ai_client import AIClient


def parse_tasks(idea_text: str, client: AIClient) -> list[dict]:
    """
    Uses the configured AI to break an idea into structured tasks.
    Returns a list of task dicts: id, title, description, type.
    """
    prompt = f"""You are a senior project manager. A user has submitted the following project idea:

\"\"\"{idea_text}\"\"\"

Break this idea into a clear, actionable list of tasks. For each task, determine:
- A short title
- A detailed description of what needs to be done
- A type: one of "research", "design", "code", "content", "review", or "other"

Respond ONLY with a valid JSON array. No markdown, no explanation. Example format:
[
  {{
    "id": 1,
    "title": "Define project scope",
    "description": "Outline the core features and boundaries of the project.",
    "type": "research"
  }}
]

Generate between 3 and 8 tasks. Be specific and practical."""

    raw = client.complete(prompt)

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
