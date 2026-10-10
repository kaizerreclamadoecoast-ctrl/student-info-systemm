"""Student model (src/models/student.py)."""

import re
import uuid
from datetime import datetime

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Student:
    """A student record. Raises ValueError when the data is invalid."""

    def __init__(self, name, email, course, year_level, gpa=0.0, student_id=None):
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = str(name).strip()
        self.email = str(email).strip().lower()
        self.course = str(course).strip()
        self.year_level = self._to_number(year_level, int, "Year level")
        self.gpa = round(self._to_number(gpa, float, "GPA"), 2)
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self._validate()

    @staticmethod
    def _to_number(value, kind, label):
        """Convert user input (often a string) to int/float or raise ValueError."""
        try:
            return kind(value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a number") from None

    def _validate(self):
        if not self.name:
            raise ValueError("Name is required")
        if not EMAIL_PATTERN.match(self.email):
            raise ValueError("Invalid email address")
        if not self.course:
            raise ValueError("Course is required")
        if not 1 <= self.year_level <= 6:
            raise ValueError("Year level must be between 1 and 6")
        if not 0.0 <= self.gpa <= 4.0:
            raise ValueError("GPA must be between 0.0 and 4.0")

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'course': self.course,
            'year_level': self.year_level,
            'gpa': self.gpa,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
