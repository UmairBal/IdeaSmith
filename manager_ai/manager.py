import json
from ai_client import AIClient, PROVIDERS
from manager_ai.task_parser import parse_tasks
import config


class ManagerAI:
    def __init__(self, provider: str = "anthropic", api_key: str = "", model: str = ""):
        self.provider = provider or "anthropic"
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        self.model = model or PROVIDERS[self.provider]["models"][0]
        self.tasks: list[dict] = []
        self.client = AIClient(self.provider, self.api_key, self.model)

    def receive_idea(self, idea_text: str) -> list[dict]:
        print(f"[ManagerAI:{self.provider}/{self.model}] Analyzing idea...")
        self.tasks = parse_tasks(idea_text, self.client)
        print(f"[ManagerAI] Generated {len(self.tasks)} tasks.")
        return self.tasks

    def review_output(self, task: dict, developer_output: str) -> dict:
        prompt = f"""You are a strict but fair project manager reviewing work done by a developer.

TASK:
Title: {task['title']}
Description: {task['description']}
Type: {task['type']}

DEVELOPER OUTPUT:
{developer_output}

Review this output. Decide:
1. Is it approved? (true/false)
2. Quality score from 1 to 10
3. Brief feedback (1-2 sentences)

Respond ONLY with valid JSON. No markdown. Example:
{{
  "approved": true,
  "score": 8,
  "feedback": "Solid work covering all required points. Could add more detail on edge cases."
}}"""

        raw = self.client.complete(prompt)
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        result["task_id"] = task["id"]
        return result

    def generate_summary(self, idea: str, results: list[dict]) -> str:
        approved = [r for r in results if r.get("approved")]
        avg_score = sum(r.get("score", 0) for r in approved) / max(len(approved), 1)

        prompt = f"""You are summarizing the outcome of an AI-powered project build session.

Original Idea: {idea}

{len(approved)} out of {len(results)} tasks were approved. Average quality score: {avg_score:.1f}/10.

Write a 2-3 sentence executive summary of what was accomplished and what the user should do next.
Be encouraging but honest."""

        return self.client.complete(prompt)
