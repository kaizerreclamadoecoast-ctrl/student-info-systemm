"""Configuration loader (src/utils/config.py).

Precedence (lowest to highest): built-in defaults, config/config.json,
then SIS_* environment variables (handy for Docker and cloud platforms).
"""

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_FILE = PROJECT_ROOT / "config" / "config.json"

DEFAULTS = {
    "data_file": "data/students.json",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}
ENV_VARS = {
    "SIS_DATA_FILE": "data_file",
    "SIS_LOG_FILE": "log_file",
    "SIS_LOG_LEVEL": "log_level",
}
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def load_config(config_path=None):
    """Return the settings as a dict. Raises ValueError if they are invalid."""
    path = Path(config_path or os.getenv("SIS_CONFIG_FILE") or DEFAULT_CONFIG_FILE)
    config = dict(DEFAULTS)

    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot read config file {path}: {exc}") from exc
        if not isinstance(loaded, dict):
            raise ValueError(f"Config file {path} must contain a JSON object")
        config.update(loaded)

    for env_name, key in ENV_VARS.items():
        if os.getenv(env_name):
            config[key] = os.environ[env_name]

    unknown = set(config) - set(DEFAULTS)
    if unknown:
        raise ValueError(f"Unknown config keys: {sorted(unknown)}")

    config["log_level"] = str(config["log_level"]).upper()
    if config["log_level"] not in VALID_LOG_LEVELS:
        raise ValueError(f"log_level must be one of {VALID_LOG_LEVELS}")

    # Relative paths are anchored to the project root, so the cwd does not matter.
    for key in ("data_file", "log_file"):
        config[key] = str(PROJECT_ROOT / config[key])
    return config
