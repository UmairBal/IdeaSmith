import json
from ai_client import AIClient, PROVIDERS
from manager_ai.task_parser import parse_tasks
from utils import extract_json
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
3. Specific feedback for improvement (be constructive and actionable)

Respond ONLY with valid JSON. No markdown. Example:
{{
  "approved": true,
  "score": 8,
  "feedback": "Solid work covering all required points. Could add more detail on edge cases."
}}"""

        raw = self.client.complete(prompt)
        result = extract_json(raw)
        result["task_id"] = task["id"]
        return result

    def generate_improvement_prompt(self, task: dict, previous_output: str, feedback: str) -> str:
        """Generate a prompt for the developer to improve based on feedback."""
        return f"""You are improving a previous work submission based on manager feedback.

ORIGINAL TASK:
Title: {task['title']}
Description: {task['description']}
Type: {task['type']}

PREVIOUS OUTPUT:
{previous_output}

MANAGER FEEDBACK FOR IMPROVEMENT:
{feedback}

Please revise and improve your work based on the feedback above. 
Keep what was good, address the specific issues mentioned.
Respond with the improved version in the same format as before."""

    def generate_summary(self, idea: str, results: list[dict]) -> str:
        approved = [r for r in results if r.get("approved")]
        avg_score = sum(r.get("score", 0) for r in approved) / max(len(approved), 1)

        task_lines = "\n".join(
            f"- [{('✅' if r.get('approved') else '❌')}] "
            f"Score {r.get('score', 'N/A')}/10 — {r.get('feedback', '').strip()}"
            for r in results
        )

        prompt = f"""You are summarizing the outcome of an AI-powered project build session.

Original Idea: {idea}

{len(approved)} out of {len(results)} tasks were approved. Average quality score: {avg_score:.1f}/10.

Task-by-task results:
{task_lines}

Write a 2-3 sentence executive summary of what was accomplished and what the user should do next.
Be encouraging but honest. Reference specific outcomes where useful."""

        return self.client.complete(prompt)
