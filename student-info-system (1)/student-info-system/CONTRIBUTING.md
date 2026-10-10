# Contributing

## Workflow
1. Open or pick an issue.
2. Branch from `main`: `feature/<short-name>` or `fix/<short-name>`.
3. Make small, focused commits using [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`).
4. Run the tests: `python -m unittest discover -s tests -t .`
5. Open a pull request using the template; CI must pass before merging.

## Code style
- Add a docstring to every module and to non-obvious functions.
- Validate input in `models/student.py` and raise `ValueError` with a clear message.
- Log with `logging.getLogger(__name__)`; show friendly messages to the user with `print`.
- Keep the layers separate: `main.py` (menu) -> `services/` (logic) -> `models/` (data rules).
