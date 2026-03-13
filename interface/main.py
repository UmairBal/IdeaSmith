import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import config
from ai_client import PROVIDERS
from manager_ai.manager import ManagerAI
from developer_ai.developer import DeveloperAI

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/providers")
def providers():
    """Return provider/model registry to the frontend."""
    return jsonify(PROVIDERS)


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    idea = data.get("idea", "").strip()

    # Manager settings
    mgr_provider = data.get("manager_provider", "anthropic")
    mgr_key      = data.get("manager_key", "").strip() or config.ANTHROPIC_API_KEY
    mgr_model    = data.get("manager_model", "").strip()

    # Developer settings
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
            yield f"event: {event}\ndata: {json.dumps(payload)}\n\n"

        try:
            yield from emit("phase", {"phase": "planning", "message": f"Manager AI ({mgr_provider} / {mgr_model}) is analyzing your idea..."})

            manager   = ManagerAI(provider=mgr_provider, api_key=mgr_key, model=mgr_model)
            developer = DeveloperAI(provider=dev_provider, api_key=dev_key, model=dev_model)

            tasks = manager.receive_idea(idea)
            yield from emit("tasks", {"tasks": tasks})

            yield from emit("phase", {"phase": "executing", "message": f"Developer AI ({dev_provider} / {dev_model}) is executing tasks..."})

            dev_results = []
            for task in tasks:
                yield from emit("task_start", {"task_id": task["id"], "title": task["title"]})
                result = developer.execute_tasks([task])[0]
                dev_results.append(result)
                yield from emit("task_done", {"task_id": task["id"], "output": result["output"]})

            yield from emit("phase", {"phase": "reviewing", "message": "Manager AI is reviewing outputs..."})

            reviews = []
            for result in dev_results:
                review = manager.review_output(result["task"], result["output"])
                reviews.append(review)
                yield from emit("review", review)

            yield from emit("phase", {"phase": "summary", "message": "Generating project summary..."})
            summary = manager.generate_summary(idea, reviews)
            yield from emit("summary", {"text": summary})
            yield from emit("done", {"message": "IdeaSmith complete!"})

        except Exception as e:
            yield from emit("error", {"message": str(e)})

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    print("🔨 IdeaSmith is running at http://localhost:5000")
    app.run(debug=config.DEBUG, port=5000)
