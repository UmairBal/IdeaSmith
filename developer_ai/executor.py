"""
executor.py — Executes individual tasks.
Code tasks return structured JSON with project files.
All other task types return plain text.
"""

import re
import json
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

# ── Prompt: ask model to use FILE SEPARATORS instead of JSON ──────────────────
# This avoids the #1 Groq failure mode: unescaped quotes inside JSON strings.
CODE_PROMPT = """You are a skilled full-stack developer. Build a complete, working project.

TASK TITLE: {title}
TASK DESCRIPTION: {description}

OUTPUT FORMAT — follow this EXACTLY:
Line 1: PROJECT_TYPE: <one of: html | react-cdn | node | python | other>
Line 2: DESCRIPTION: <one sentence describing what was built>
Line 3: ENTRY_POINT: <filename to open/run first, e.g. index.html or app.py>
Line 4: RUN_COMMAND: <command to start the project>
Line 5: NPM_DEPS: <comma-separated npm packages, or NONE>
Line 6: PIP_DEPS: <comma-separated pip packages, or NONE>
Line 7: blank line
Then list each file using this separator pattern:

===FILE: path/to/filename.ext===
<complete file content here>
===END===

Rules:
- React: Use React 18 + ReactDOM + Babel Standalone CDN. Single self-contained HTML file. JSX in <script type="text/babel">.
- HTML: Beautiful, complete, self-contained HTML/CSS/JS in one file.
- Node: Include package.json + all source files.
- Python: Include requirements.txt + main script.
- Write COMPLETE file contents. No placeholders, no "// TODO", no truncation.
- Include ALL files needed to run the project."""


def _parse_file_format(raw: str) -> dict:
    """
    Parse the FILE SEPARATOR format:
      PROJECT_TYPE: html
      DESCRIPTION: ...
      ENTRY_POINT: index.html
      RUN_COMMAND: open index.html
      NPM_DEPS: NONE
      PIP_DEPS: NONE

      ===FILE: index.html===
      <content>
      ===END===
    """
    lines = raw.strip().splitlines()
    meta = {}
    for line in lines[:10]:
        if ':' in line:
            key, _, val = line.partition(':')
            meta[key.strip().upper()] = val.strip()

    files = []
    pattern = re.compile(r'===FILE:\s*(.+?)===\s*\n([\s\S]*?)\n===END===', re.MULTILINE)
    for match in pattern.finditer(raw):
        path = match.group(1).strip()
        file_content = match.group(2)
        files.append({"path": path, "content": file_content})

    def parse_deps(val):
        if not val or val.upper() in ('NONE', 'N/A', ''):
            return []
        return [d.strip() for d in val.split(',') if d.strip() and d.strip().upper() != 'NONE']

    return {
        "project_type": meta.get("PROJECT_TYPE", "other").lower(),
        "description": meta.get("DESCRIPTION", ""),
        "entry_point": meta.get("ENTRY_POINT", files[0]["path"] if files else ""),
        "run_command": meta.get("RUN_COMMAND", ""),
        "files": files,
        "dependencies": {
            "npm": parse_deps(meta.get("NPM_DEPS", "")),
            "pip": parse_deps(meta.get("PIP_DEPS", "")),
        },
    }


def _try_json_parse(raw: str) -> dict | None:
    """Try extracting JSON — returns None on failure instead of raising."""
    try:
        data = extract_json(raw)
        if isinstance(data, dict) and data.get("files"):
            return data
    except Exception:
        pass
    return None


def _fallback_single_file(raw: str, task_title: str) -> dict:
    """
    Last resort: wrap the entire raw response as a single HTML file.
    This ensures something always gets saved even if parsing fully fails.
    """
    # Try to detect if it looks like HTML
    if re.search(r'<html|<!DOCTYPE', raw, re.IGNORECASE):
        # Extract just the HTML portion
        html_match = re.search(r'(<!DOCTYPE[\s\S]*?</html>)', raw, re.IGNORECASE)
        file_content = html_match.group(1) if html_match else raw
        filename = "index.html"
        project_type = "html"
    else:
        # Wrap as a readable HTML page showing the output
        escaped = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        file_content = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{task_title}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px;
         background: #0d1117; color: #e6edf3; line-height: 1.7; }}
  pre {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px;
        padding: 20px; white-space: pre-wrap; word-break: break-word; font-size: 13px; }}
  h1 {{ color: #a855f7; }}
</style></head>
<body>
<h1>{task_title}</h1>
<pre>{escaped}</pre>
</body></html>"""
        filename = "output.html"
        project_type = "html"

    return {
        "project_type": project_type,
        "description": f"Output for: {task_title}",
        "entry_point": filename,
        "run_command": f"Open {filename} in your browser",
        "files": [{"path": filename, "content": file_content}],
        "dependencies": {"npm": [], "pip": []},
    }


def execute_task(task: dict, client: AIClient) -> dict:
    """
    Returns:
      {"type": "files",  "project": {...}}
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

        # Strategy 1: Try the FILE SEPARATOR format (primary — works for all providers)
        try:
            project_data = _parse_file_format(raw)
            if project_data["files"]:
                return {"type": "files", "project": project_data}
        except Exception:
            pass

        # Strategy 2: Try JSON (works for Anthropic/OpenAI)
        project_data = _try_json_parse(raw)
        if project_data:
            project_data.setdefault("files", [])
            project_data.setdefault("dependencies", {"npm": [], "pip": []})
            project_data.setdefault("project_type", "other")
            project_data.setdefault("entry_point", "")
            project_data.setdefault("run_command", "")
            return {"type": "files", "project": project_data}

        # Strategy 3: Fallback — wrap raw output as viewable HTML
        project_data = _fallback_single_file(raw, task["title"])
        return {"type": "files", "project": project_data}

    # Non-code tasks
    instruction = TYPE_INSTRUCTIONS.get(task_type, TYPE_INSTRUCTIONS["other"])
    prompt = f"""You are a skilled specialist. Complete the following task:

TASK TITLE: {task['title']}
TASK DESCRIPTION: {task['description']}
TASK TYPE: {task_type}

INSTRUCTIONS: {instruction}

Complete this task thoroughly, specifically, and with high quality. Format your response clearly."""

    content = client.complete(prompt, max_tokens=max_tokens)
    return {"type": "text", "content": content}
