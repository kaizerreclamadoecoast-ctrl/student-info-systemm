import json
import tempfile
import unittest
from pathlib import Path

from services.student_service import StudentService

DATA = dict(name="Ada Lovelace", email="ada@example.com", course="Computer Science", year_level="2")


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "nested" / "students.json"
        self.service = StudentService(str(self.path))

    def test_creates_data_file(self):
        self.assertEqual(json.loads(self.path.read_text()), [])

    def test_add_and_get(self):
        added = self.service.add_student(dict(DATA))
        self.assertEqual(self.service.get_student(added['student_id'])['name'], "Ada Lovelace")
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.service.get_student("nope"))

    def test_duplicate_email_rejected(self):
        self.service.add_student(dict(DATA))
        with self.assertRaises(ValueError):
            self.service.add_student(dict(DATA))

    def test_invalid_data_not_saved(self):
        with self.assertRaises(ValueError):
            self.service.add_student({**DATA, "email": "bad"})
        self.assertEqual(self.service.get_all_students(), [])

    def test_update(self):
        sid = self.service.add_student(dict(DATA))['student_id']
        updated = self.service.update_student(sid, {"course": "Mathematics", "gpa": "3.8"})
        self.assertEqual((updated['course'], updated['gpa']), ("Mathematics", 3.8))
        self.assertEqual(self.service.get_student(sid)['course'], "Mathematics")

    def test_update_ignores_protected_fields(self):
        sid = self.service.add_student(dict(DATA))['student_id']
        self.service.update_student(sid, {"student_id": "HACK", "name": "Ada L."})
        self.assertIsNotNone(self.service.get_student(sid))
        self.assertIsNone(self.service.get_student("HACK"))

    def test_update_validates_and_checks_email(self):
        first = self.service.add_student(dict(DATA))['student_id']
        second = self.service.add_student({**DATA, "email": "b@example.com"})['student_id']
        with self.assertRaises(ValueError):
            self.service.update_student(first, {"gpa": "9"})
        with self.assertRaises(ValueError):
            self.service.update_student(second, {"email": "ada@example.com"})
        self.assertEqual(self.service.get_student(first)['gpa'], 0.0)

    def test_update_missing_returns_none(self):
        self.assertIsNone(self.service.update_student("nope", {"name": "X"}))

    def test_delete(self):
        sid = self.service.add_student(dict(DATA))['student_id']
        self.assertTrue(self.service.delete_student(sid))
        self.assertFalse(self.service.delete_student(sid))
        self.assertEqual(self.service.get_all_students(), [])

    def test_corrupt_file_is_preserved(self):
        self.path.write_text("{ not json")
        with self.assertLogs("services.student_service", level="ERROR"):
            self.assertEqual(self.service.get_all_students(), [])
        self.assertTrue(Path(str(self.path) + ".corrupt").exists())


if __name__ == "__main__":
    unittest.main()
