import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from utils.config import PROJECT_ROOT, load_config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def load(self, content=None, env=None):
        path = self.dir / "config.json"
        if content is not None:
            path.write_text(content)
        with mock.patch.dict(os.environ, env or {}, clear=True):
            return load_config(str(path))

    def test_defaults_when_file_missing(self):
        config = self.load()
        self.assertEqual(config['data_file'], str(PROJECT_ROOT / "data/students.json"))
        self.assertEqual(config['log_level'], "INFO")

    def test_file_overrides_defaults_and_env_overrides_file(self):
        self.assertEqual(self.load('{"log_level": "debug"}')['log_level'], "DEBUG")
        config = self.load('{"log_level": "debug"}', env={"SIS_LOG_LEVEL": "error"})
        self.assertEqual(config['log_level'], "ERROR")

    def test_absolute_paths_are_kept(self):
        config = self.load(env={"SIS_DATA_FILE": "/data/students.json"})
        self.assertEqual(config['data_file'], "/data/students.json")

    def test_invalid_config_raises(self):
        for content in ("{ bad json", "[1, 2]", '{"log_level": "LOUD"}', '{"colour": "red"}'):
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.load(content)


if __name__ == "__main__":
    unittest.main()
