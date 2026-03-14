"""
file_manager.py — Handles project file creation, tree building, and dependency installation.
"""

import os
import subprocess

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")


def get_project_path(session_id: str) -> str:
    path = os.path.join(PROJECTS_DIR, session_id)
    os.makedirs(path, exist_ok=True)
    return path


def save_files(session_id: str, files: list) -> str:
    """Write all project files to disk, creating directories as needed."""
    project_path = get_project_path(session_id)
    for f in files:
        rel_path = f["path"].lstrip("/").lstrip("\\")
        file_path = os.path.join(project_path, rel_path)
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as fp:
            fp.write(f["content"])
    return project_path


def get_file_tree(session_id: str) -> list:
    project_path = get_project_path(session_id)
    if not os.path.exists(project_path):
        return []
    return _walk_tree(project_path, project_path)


SKIP_DIRS = {"node_modules", "__pycache__", ".git", ".DS_Store", "venv", ".venv", "dist", "build"}


def _walk_tree(base: str, current: str) -> list:
    result = []
    try:
        entries = sorted(
            os.scandir(current),
            key=lambda e: (not e.is_dir(), e.name.lower())
        )
        for entry in entries:
            if entry.name in SKIP_DIRS or entry.name.startswith("."):
                continue
            rel = os.path.relpath(entry.path, base).replace("\\", "/")
            node = {"name": entry.name, "path": rel}
            if entry.is_dir():
                node["type"] = "dir"
                node["children"] = _walk_tree(base, entry.path)
            else:
                node["type"] = "file"
                node["size"] = entry.stat().st_size
            result.append(node)
    except PermissionError:
        pass
    return result


def get_file_content(session_id: str, file_path: str) -> str:
    project_path = get_project_path(session_id)
    safe_path = file_path.lstrip("/").lstrip("\\")
    full_path = os.path.join(project_path, safe_path)
    # Safety: ensure file is inside project directory
    full_path = os.path.realpath(full_path)
    project_path = os.path.realpath(project_path)
    if not full_path.startswith(project_path):
        raise PermissionError("Path traversal detected")
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def install_dependencies(session_id: str, deps: dict) -> dict:
    """Run npm install and/or pip install for given dependency lists."""
    project_path = get_project_path(session_id)
    results = {}

    if deps.get("npm"):
        try:
            result = subprocess.run(
                ["npm", "install"] + deps["npm"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120,
            )
            results["npm"] = {
                "success": result.returncode == 0,
                "output": (result.stdout + result.stderr).strip(),
            }
        except FileNotFoundError:
            results["npm"] = {"success": False, "output": "npm not found. Please install Node.js."}
        except Exception as e:
            results["npm"] = {"success": False, "output": str(e)}

    if deps.get("pip"):
        try:
            result = subprocess.run(
                ["pip", "install", "--break-system-packages"] + deps["pip"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            results["pip"] = {
                "success": result.returncode == 0,
                "output": (result.stdout + result.stderr).strip(),
            }
        except Exception as e:
            results["pip"] = {"success": False, "output": str(e)}

    return results
