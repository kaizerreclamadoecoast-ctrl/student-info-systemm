"""Student service (src/services/student_service.py): CRUD stored in a JSON file."""

import json
import logging
import os
from datetime import datetime

from models.student import Student

logger = logging.getLogger(__name__)

# Fields that update_student() is allowed to change (the ID and timestamps are protected).
UPDATABLE_FIELDS = ('name', 'email', 'course', 'year_level', 'gpa')


class StudentService:
    def __init__(self, data_file='data/students.json'):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(self.data_file) or '.', exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_students(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Keep the unreadable file instead of silently overwriting it on the next save.
            backup = f"{self.data_file}.corrupt"
            os.replace(self.data_file, backup)
            logger.error("Data file is not valid JSON; moved to %s, starting empty", backup)
            return []

    def _save_students(self, students):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=2)

    @staticmethod
    def _email_taken(students, email, exclude_id=None):
        return any(s['email'] == email and s['student_id'] != exclude_id for s in students)

    def add_student(self, student_data):
        students = self._load_students()
        student = Student(**student_data)
        if self._email_taken(students, student.email):
            raise ValueError(f"Email '{student.email}' is already registered")
        students.append(student.to_dict())
        self._save_students(students)
        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        students = self._load_students()
        for student in students:
            if student['student_id'] == student_id:
                return student
        return None

    def update_student(self, student_id, update_data):
        students = self._load_students()
        for student in students:
            if student['student_id'] == student_id:
                changes = {k: v for k, v in update_data.items() if k in UPDATABLE_FIELDS}
                current = {k: student[k] for k in UPDATABLE_FIELDS}
                checked = Student(student_id=student_id, **{**current, **changes})  # validates
                if self._email_taken(students, checked.email, exclude_id=student_id):
                    raise ValueError(f"Email '{checked.email}' is already registered")
                student.update({k: getattr(checked, k) for k in UPDATABLE_FIELDS})
                student['updated_at'] = datetime.now().isoformat()
                self._save_students(students)
                return student
        return None

    def delete_student(self, student_id):
        students = self._load_students()
        remaining = [s for s in students if s['student_id'] != student_id]
        if len(remaining) == len(students):
            return False
        self._save_students(remaining)
        return True
