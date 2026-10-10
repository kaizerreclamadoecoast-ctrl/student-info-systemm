import contextlib
import io
import logging
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from main import StudentInformationSystem
from services.student_service import StudentService


class MenuTests(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.addCleanup(logging.disable, logging.NOTSET)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.service = StudentService(str(Path(tmp.name) / "students.json"))
        self.app = StudentInformationSystem(self.service)

    def run_menu(self, *answers):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(answers)), contextlib.redirect_stdout(out):
            self.app.run()
        return out.getvalue()

    def test_add_view_update_delete_flow(self):
        out = self.run_menu("1", "Ada", "ada@example.com", "CS", "2", "2", "6")
        self.assertIn("Student added successfully", out)
        self.assertIn("Name: Ada", out)

        sid = self.service.get_all_students()[0]['student_id']
        out = self.run_menu("3", sid, "4", sid, "Ada L.", "", "", "", "3.5", "6")
        self.assertIn("Student updated successfully", out)
        self.assertEqual(self.service.get_student(sid)['name'], "Ada L.")

        out = self.run_menu("5", sid, "y", "6")
        self.assertIn("Student deleted successfully", out)
        self.assertEqual(self.service.get_all_students(), [])

    def test_invalid_input_shows_error(self):
        out = self.run_menu("1", "Ada", "bad-email", "CS", "2", "6")
        self.assertIn("Error adding student: Invalid email address", out)
        self.assertEqual(self.service.get_all_students(), [])

    def test_delete_can_be_cancelled(self):
        sid = self.service.add_student(dict(name="A", email="a@b.co", course="C", year_level=1))['student_id']
        out = self.run_menu("5", sid, "n", "6")
        self.assertIn("Cancelled", out)
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_not_found_and_invalid_choice(self):
        out = self.run_menu("3", "zzz", "4", "zzz", "5", "zzz", "9", "6")
        self.assertEqual(out.count("Student not found."), 3)
        self.assertIn("Invalid choice", out)


if __name__ == "__main__":
    unittest.main()
