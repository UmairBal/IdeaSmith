from developer_ai.executor import execute_task, improve_task
from ai_client import AIClient, PROVIDERS
import config


class DeveloperAI:
    def __init__(self, provider: str = "anthropic", api_key: str = "", model: str = ""):
        self.provider = provider or "anthropic"
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        models = PROVIDERS[self.provider]["models"]
        self.model = model or (models[1] if len(models) > 1 else models[0])
        self.client = AIClient(self.provider, self.api_key, self.model)

    def execute_tasks(self, tasks: list[dict], feedback: str = None) -> list[dict]:
        """Execute tasks. If feedback is provided, improve based on it."""
        results = []
        for task in tasks:
            if feedback:
                print(f"[DeveloperAI:{self.provider}/{self.model}] Improving task {task['id']}: {task['title']}")
                output = improve_task(task, feedback, self.client)
            else:
                print(f"[DeveloperAI:{self.provider}/{self.model}] Executing task {task['id']}: {task['title']}")
                output = execute_task(task, self.client)
            results.append({"task_id": task["id"], "task": task, "output": output})
        return results
