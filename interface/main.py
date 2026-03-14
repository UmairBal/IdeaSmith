import sys
import os
import uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
import json
import config
from ai_client import PROVIDERS
from manager_ai.manager import ManagerAI
from developer_ai.developer import DeveloperAI
from file_manager import save_files, get_file_tree, get_file_content, install_dependencies, get_project_path

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/providers")
def providers():
    return jsonify(PROVIDERS)


@app.route("/project/<session_id>/tree")
def project_tree(session_id):
    tree = get_file_tree(session_id)
    return jsonify(tree)


@app.route("/project/<session_id>/file/<path:filepath>")
def project_file(session_id, filepath):
    try:
        content = get_file_content(session_id, filepath)
        return jsonify({"content": content, "path": filepath})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/project/<session_id>/preview/<path:filepath>")
def project_preview(session_id, filepath):
    project_path = get_project_path(session_id)
    return send_from_directory(project_path, filepath)


@app.route("/project/<session_id>/install", methods=["POST"])
def project_install(session_id):
    data = request.get_json()
    deps = data.get("dependencies", {})
    results = install_dependencies(session_id, deps)
    return jsonify(results)


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    idea = data.get("idea", "").strip()
    session_id = str(uuid.uuid4())

    mgr_provider = data.get("manager_provider", "anthropic")
    mgr_key      = data.get("manager_key", "").strip() or config.ANTHROPIC_API_KEY
    mgr_model    = data.get("manager_model", "").strip()

    dev_provider = data.get("developer_provider", "anthropic")
    dev_key      = data.get("developer_key", "").strip() or config.ANTHROPIC_API_KEY
    dev_model    = data.get("developer_model", "").strip()

    if not idea:
        return jsonify({"error": "No idea provided"}), 400
    if not mgr_key:
        return jsonify({"error": "No Manager AI API key provided."}), 400
    if not dev_key:
        return jsonify({"error": "No Developer AI API key provided."}), 400

    def generate():
        def emit(event: str, payload: dict):
            # Encode payload to avoid issues with special characters in content
            data = json.dumps(payload, ensure_ascii=False)
            yield f"event: {event}\ndata: {data}\n\n"

        yield from emit("session", {"session_id": session_id})

        try:
            yield from emit("phase", {
                "phase": "planning",
                "message": f"Manager AI ({mgr_provider}/{mgr_model or 'default'}) is analyzing your idea..."
            })

            manager   = ManagerAI(provider=mgr_provider, api_key=mgr_key, model=mgr_model)
            developer = DeveloperAI(provider=dev_provider, api_key=dev_key, model=dev_model)

            tasks = manager.receive_idea(idea)
            yield from emit("tasks", {"tasks": tasks})

            yield from emit("phase", {
                "phase": "executing",
                "message": f"Developer AI ({dev_provider}/{dev_model or 'default'}) is executing tasks..."
            })

            dev_results = []
            for task in tasks:
                yield from emit("task_start", {"task_id": task["id"], "title": task["title"]})
                result = developer.execute_tasks([task])[0]
                output = result["output"]

                # Save files if this is a code task with file output
                if output.get("type") == "files" and output.get("project", {}).get("files"):
                    project = output["project"]
                    save_files(session_id, project["files"])
                    tree = get_file_tree(session_id)
                    yield from emit("files_updated", {
                        "tree": tree,
                        "project": project,
                        "task_id": task["id"],
                    })

                dev_results.append(result)
                yield from emit("task_done", {
                    "task_id": task["id"],
                    "output": output,
                })

            yield from emit("phase", {"phase": "reviewing", "message": "Manager AI is reviewing outputs..."})

            reviews = []
            for result in dev_results:
                output = result["output"]
                review_content = (
                    output["project"].get("description", "Code project generated.")
                    if output.get("type") == "files"
                    else output.get("content", "")
                )
                review = manager.review_output(result["task"], review_content)
                reviews.append(review)
                yield from emit("review", review)

            yield from emit("phase", {"phase": "summary", "message": "Generating project summary..."})
            summary = manager.generate_summary(idea, reviews)
            yield from emit("summary", {"text": summary})
            yield from emit("done", {"message": "IdeaSmith complete!", "session_id": session_id})

        except Exception as e:
            yield from emit("error", {"message": str(e)})

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "Transfer-Encoding": "chunked",
        },
    )


if __name__ == "__main__":
    print("🔨 IdeaSmith is running at http://localhost:5000")
    app.run(debug=config.DEBUG, port=5000)
