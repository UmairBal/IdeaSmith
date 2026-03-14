# ⚒ IdeaSmith

**Forge your ideas into reality — no coding required.**

IdeaSmith is an open-source dual-AI system powered by Claude. Users share their vision in plain language and two AI agents handle the rest:

- **Manager AI** (Claude Opus) — Understands your idea, breaks it into tasks, and reviews every output.
- **Developer AI** (Claude Sonnet) — Executes each task and produces real, detailed deliverables.

## Features
- 🔨 Real AI-powered task parsing (not rule-based)
- ⚙️ Per-task type execution (research, design, code, content, review)
- ✅ Automated quality review with scoring
- 🌐 Beautiful web UI with live streaming progress
- 🔑 Bring your own Anthropic API key

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/IdeaSmith.git
cd IdeaSmith
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...

python interface/main.py
```

Open http://localhost:5000 in your browser.

## How It Works

1. You type a project idea in plain language
2. **Manager AI** breaks it into 3–8 structured tasks
3. **Developer AI** executes each task in sequence
4. **Manager AI** reviews and scores each output (1–10)
5. A final summary is generated with next steps

## Project Structure

```
IdeaSmith/
├── manager_ai/
│   ├── manager.py        # ManagerAI class (parse, review, summarize)
│   └── task_parser.py    # Claude-powered task decomposition
├── developer_ai/
│   ├── developer.py      # DeveloperAI class
│   └── executor.py       # Claude-powered task execution
├── interface/
│   ├── main.py           # Flask web server + SSE streaming
│   └── templates/
│       └── index.html    # Web UI
├── config.py             # Model & key configuration
├── requirements.txt
└── .env.example
```

## Configuration

Edit `config.py` to change models:

```python
MANAGER_MODEL  = "claude-opus-4-5-20251101"    # Smarter, for planning
DEVELOPER_MODEL = "claude-sonnet-4-5-20251101" # Faster, for execution
```

## Contributing

Contributions welcome! See CONTRIBUTING.md.

## License

MIT
