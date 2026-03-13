from developer_ai.executor import execute_task
from ai_client import AIClient, PROVIDERS
import config


class DeveloperAI:
    def __init__(self, provider: str = "anthropic", api_key: str = "", model: str = ""):
        self.provider = provider or "anthropic"
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        self.model = model or PROVIDERS[self.provider]["models"][1]  # default: second model (faster)
        self.client = AIClient(self.provider, self.api_key, self.model)

    def execute_tasks(self, tasks: list[dict]) -> list[dict]:
        results = []
        for task in tasks:
            print(f"[DeveloperAI:{self.provider}/{self.model}] Executing task {task['id']}: {task['title']}")
            output = execute_task(task, self.client)
            results.append({"task_id": task["id"], "task": task, "output": output})
        return results
