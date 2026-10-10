import sys
from pathlib import Path

# Make `models`, `services`, `utils` and `main` importable, as when running src/main.py.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
