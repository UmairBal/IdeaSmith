from ai_client import AIClient

TYPE_INSTRUCTIONS = {
    "research": "Produce a thorough research brief with key findings, insights, and recommendations.",
    "design":   "Describe a detailed design plan including structure, components, style guidelines, and rationale.",
    "code":     "Write complete, well-commented, production-ready code with usage instructions.",
    "content":  "Write polished, audience-appropriate content that is clear, engaging, and complete.",
    "review":   "Provide a detailed review with specific strengths, weaknesses, and actionable improvements.",
    "other":    "Complete the task thoroughly and professionally.",
}


def execute_task(task: dict, client: AIClient) -> str:
    task_type = task.get("type", "other")
    instruction = TYPE_INSTRUCTIONS.get(task_type, TYPE_INSTRUCTIONS["other"])

    prompt = f"""You are a skilled developer and specialist. Your job is to complete the following task:

TASK TITLE: {task['title']}
TASK DESCRIPTION: {task['description']}
TASK TYPE: {task_type}

INSTRUCTIONS: {instruction}

Complete this task now. Be thorough, specific, and high-quality. Format your response clearly."""

    return client.complete(prompt)
