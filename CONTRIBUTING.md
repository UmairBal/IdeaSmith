# Contributing to IdeaSmith

Thanks for considering contributing! This project is intentionally simple (MVP) so it’s easy to extend.

## How to contribute

- **Report bugs**: Open an issue describing expected vs actual behavior and include reproduction steps.
- **Suggest features**: Open an issue with a clear use case and proposed API/UX.
- **Submit code**:
  - Fork the repo
  - Create a feature branch
  - Make changes with clear comments/docstrings
  - Open a pull request describing what changed and why

## Development notes

- **Python**: Keep code Python 3 compatible.
- **Simplicity first**: Prefer clear, readable code over clever abstractions.
- **Extensibility**: Add small, well-named functions/classes that are easy to swap for real AI calls later.

## Ideas for contributions

- **Real LLM integration**: Replace MVP stubs with actual model calls (e.g., OpenAI) in `task_parser.py` and `executor.py`.
- **Task schemas**: Introduce structured tasks (IDs, dependencies, priority, estimates).
- **Review policies**: Add richer review/approval logic in `ManagerAI.review_output`.
- **Interfaces**:
  - Web API via FastAPI
  - Web UI via Flask templates or a frontend
- **Persistence**: Save sessions and outputs to JSON files.
- **Testing**: Add unit tests for task parsing and pipeline behavior.

