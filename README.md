# IdeaSmith

**IdeaSmith** is a minimal open-source **dual-AI** project scaffold where a **Manager AI** supervises a **Developer AI** to turn plain-language project ideas into concrete outputs.

This repository is an MVP (minimum viable prototype) designed to be easy to understand and extend.

## MVP workflow

1. **User provides an idea** (plain text) via CLI.
2. **ManagerAI** parses the idea into a list of tasks.
3. **DeveloperAI** executes each task (MVP: returns a simple completion string).
4. **ManagerAI** reviews each output (MVP: approves).
5. The CLI prints a final, task-by-task report.

## Project structure

```
IdeaSmith/
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── manager_ai/
│   ├── manager.py
│   └── task_parser.py
├── developer_ai/
│   ├── developer.py
│   └── executor.py
├── interface/
│   └── main.py
└── examples/
    └── example_idea.json
```

## Quick start (MVP)

### 1) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2) Run the CLI

```bash
python interface/main.py
```

Then paste a project idea and press Enter. Use an empty line to finish multi-line input.

## Contributing

See `CONTRIBUTING.md` for how to contribute and ideas for improvements.

