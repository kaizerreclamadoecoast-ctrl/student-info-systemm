# Changelog

## [1.1.0] - 2026-10-10
### Changed
- Switched to the course sample implementation: `Student` model, `StudentService`
  and the `StudentInformationSystem` interactive menu in `src/main.py`
- Records now use a single `name` field and an auto-generated 8-character ID
### Added
- Update and delete menu options (were placeholders in the sample)
- Input validation, duplicate-email check, config file with env overrides
### Fixed
- Relative import in the service, missing `datetime` import, missing `student_id`
  when adding, and `delete_student` always returning `False`

## [1.0.0] - 2026-10-10
### Added
- CRUD operations for students (add, list/search, view, update, delete)
- JSON and XML storage backends with atomic writes
- Layered configuration (defaults, config file, environment variables)
- Rotating file logging
- Interactive menu and argparse CLI
- Unit tests, GitHub Actions CI, Dockerfile
