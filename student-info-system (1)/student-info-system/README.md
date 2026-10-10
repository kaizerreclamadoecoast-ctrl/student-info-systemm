# student-info-system

[![CI](https://github.com/<your-username>/student-info-system/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/student-info-system/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A menu-driven Student Information System written in Python. Student records are
stored in a JSON file. The app uses only the standard library, is configured
through a file or environment variables, and writes a log file, so it runs the
same on a laptop, in Docker, or on a cloud platform.

## Features
- **Create, read, update, delete** students from an interactive menu
- View all students, or one student by ID
- Validation: name and course required, valid email, year level 1-6, GPA 0-4, unique email
- JSON storage in `data/students.json`
- Logging to `logs/app.log` and the console
- Friendly error messages; invalid input never crashes the program

## Project structure
```
student-info-system/
├── src/
│   ├── models/student.py            # Student model + validation
│   ├── services/student_service.py  # CRUD operations on the JSON file
│   ├── utils/config.py              # configuration loader
│   └── main.py                      # interactive menu (entry point)
├── data/students.json               # student records (sample data included)
├── config/config.json               # settings
├── logs/                            # log files (git-ignored)
├── tests/                           # unittest suite
├── README.md
├── requirements.txt
└── .gitignore
```
Flow: `main.py (menu) -> StudentService -> Student model`, with data kept in a JSON file.

## Getting started
```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python src/main.py          # Python 3.10+, nothing to install
```

## Usage
```
=== Student Information System ===
1. Add Student
2. View All Students
3. View Student by ID
4. Update Student        (press Enter to keep a field's current value)
5. Delete Student        (asks for confirmation)
6. Exit
```

### Data format (`data/students.json`)
```json
{
  "student_id": "S-001",
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "course": "Computer Science",
  "year_level": 2,
  "gpa": 3.9,
  "created_at": "2026-10-10T09:00:00",
  "updated_at": "2026-10-10T09:00:00"
}
```
New students get an automatic 8-character ID.

## Configuration
Precedence: **defaults < `config/config.json` < environment variables**.
Relative paths are resolved from the project root.

| Setting | Env variable | Default | Description |
|---|---|---|---|
| `data_file` | `SIS_DATA_FILE` | `data/students.json` | Where records are stored |
| `log_file` | `SIS_LOG_FILE` | `logs/app.log` | Log file |
| `log_level` | `SIS_LOG_LEVEL` | `INFO` | DEBUG, INFO, WARNING, ERROR, CRITICAL |

Use `SIS_CONFIG_FILE` to load a different config file. See `.env.example`.

## Docker / cloud
```bash
docker build -t student-info-system .
docker run -it --rm -v sis-data:/data student-info-system
```
The container runs as a non-root user and keeps its records only in the `/data`
volume, so it fits AWS ECS, Azure Container Apps or Google Cloud Run with a volume.

## Error handling
- Invalid input raises `ValueError` in the model; the menu shows the message and logs it.
- A missing data file is created automatically.
- A corrupt data file is moved to `students.json.corrupt` instead of being overwritten.
- A bad config file stops the app with a clear message.

## Testing
```bash
python -m unittest discover -s tests -t . -v
```
GitHub Actions runs the tests on Python 3.10-3.12 for every push and pull request.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md). Licensed under MIT.
