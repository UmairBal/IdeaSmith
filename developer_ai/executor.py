"""
executor.py — Executes individual tasks.
Code tasks return structured JSON with project files.
All other task types return plain text.
"""

from ai_client import AIClient
from utils import extract_json

TYPE_INSTRUCTIONS = {
    "research": "Produce a thorough research brief with key findings, insights, and recommendations.",
    "design":   "Describe a detailed design plan including structure, components, style guidelines, and rationale.",
    "content":  "Write polished, audience-appropriate content that is clear, engaging, and complete.",
    "review":   "Provide a detailed review with specific strengths, weaknesses, and actionable improvements.",
    "other":    "Complete the task thoroughly and professionally.",
}

TYPE_MAX_TOKENS = {
    "code":     4096,
    "design":   3000,
    "research": 3000,
    "content":  2500,
    "review":   2000,
    "other":    2000,
}

CODE_PROMPT = """You are a skilled full-stack developer. Build a complete, working project for this task.

TASK TITLE: {title}
TASK DESCRIPTION: {description}

Output ONLY a valid JSON object — no markdown, no explanation, nothing else. Use this exact structure:
{{
  "project_type": "html|react-cdn|node|python|other",
  "description": "what was built, 1-2 sentences",
  "files": [
    {{"path": "index.html", "content": "full file content here"}}
  ],
  "dependencies": {{
    "npm": [],
    "pip": []
  }},
  "entry_point": "index.html",
  "run_command": "how to run this project"
}}

CRITICAL RULES:
- React projects: Use React 18 + ReactDOM + Babel Standalone from CDN (unpkg or cdnjs). No build tools. All JSX in a single HTML file using <script type="text/babel">.
- HTML projects: Complete, beautiful, self-contained HTML/CSS/JS.
- Node.js projects: Include package.json (with "main" field) + all source files.
- Python projects: Include requirements.txt + main script.
- Every file must be 100% complete — no placeholders, no "// TODO", no "..." truncations.
- List only EXTERNAL packages in dependencies (e.g. "express", "flask") — not built-ins.
- Output ONLY the JSON object. No text before or after."""


def execute_task(task: dict, client: AIClient) -> dict:
    """
    Returns one of:
      {"type": "files",  "project": {project_type, description, files, dependencies, entry_point, run_command}}
      {"type": "text",   "content": str}
    """
    task_type = task.get("type", "other")
    max_tokens = TYPE_MAX_TOKENS.get(task_type, 2000)

    if task_type == "code":
        prompt = CODE_PROMPT.format(
            title=task["title"],
            description=task["description"],
        )
        raw = client.complete(prompt, max_tokens=max_tokens)
        try:
            project_data = extract_json(raw)
            project_data.setdefault("files", [])
            project_data.setdefault("dependencies", {"npm": [], "pip": []})
            project_data.setdefault("project_type", "other")
            project_data.setdefault("entry_point", "")
            project_data.setdefault("run_command", "")
            return {"type": "files", "project": project_data}
        except Exception:
            return {"type": "text", "content": raw}

    instruction = TYPE_INSTRUCTIONS.get(task_type, TYPE_INSTRUCTIONS["other"])
    prompt = f"""You are a skilled specialist. Complete the following task:

TASK TITLE: {task['title']}
TASK DESCRIPTION: {task['description']}
TASK TYPE: {task_type}

INSTRUCTIONS: {instruction}

Complete this task thoroughly, specifically, and with high quality. Format your response clearly."""

    content = client.complete(prompt, max_tokens=max_tokens)
    return {"type": "text", "content": content}
