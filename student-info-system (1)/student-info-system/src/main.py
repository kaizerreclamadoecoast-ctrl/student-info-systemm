"""Student Information System (src/main.py): interactive menu application.

Run from anywhere:
    python src/main.py
"""

import logging
import os
import sys

from services.student_service import StudentService
from utils.config import load_config


def setup_logging(config):
    """Log to the file named in the config and to the console."""
    os.makedirs(os.path.dirname(config['log_file']), exist_ok=True)
    logging.basicConfig(
        level=config['log_level'],
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config['log_file'], encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


class StudentInformationSystem:
    def __init__(self, student_service=None):
        self.student_service = student_service or StudentService()
        self.logger = logging.getLogger(__name__)

    def display_menu(self):
        print("\n=== Student Information System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

    def add_student(self):
        print("\n--- Add New Student ---")
        name = input("Name: ")
        email = input("Email: ")
        course = input("Course: ")
        year_level = input("Year Level: ")

        student_data = {
            'name': name,
            'email': email,
            'course': course,
            'year_level': year_level
        }

        try:
            student = self.student_service.add_student(student_data)
            self.logger.info("Added student: %s", student['student_id'])
            print(f"Student added successfully! ID: {student['student_id']}")
        except Exception as e:
            self.logger.error("Error adding student: %s", e)
            print(f"Error adding student: {e}")

    def view_all_students(self):
        print("\n--- All Students ---")
        students = self.student_service.get_all_students()
        if not students:
            print("No students found.")
            return

        for student in students:
            print(f"ID: {student['student_id']}, Name: {student['name']}, "
                  f"Email: {student['email']}, Course: {student['course']}")

    def view_student(self):
        student_id = input("Enter Student ID: ").strip()
        student = self.student_service.get_student(student_id)
        if student:
            print(f"\nStudent Details: {student}")
        else:
            print("Student not found.")

    def update_student(self):
        print("\n--- Update Student ---")
        student_id = input("Enter Student ID: ").strip()
        student = self.student_service.get_student(student_id)
        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep the current value.")
        update_data = {}
        for field, label in (('name', 'Name'), ('email', 'Email'), ('course', 'Course'),
                             ('year_level', 'Year Level'), ('gpa', 'GPA')):
            value = input(f"{label} [{student[field]}]: ").strip()
            if value:
                update_data[field] = value

        if not update_data:
            print("No changes made.")
            return

        try:
            self.student_service.update_student(student_id, update_data)
            self.logger.info("Updated student: %s", student_id)
            print("Student updated successfully!")
        except Exception as e:
            self.logger.error("Error updating student %s: %s", student_id, e)
            print(f"Error updating student: {e}")

    def delete_student(self):
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID: ").strip()
        if not self.student_service.get_student(student_id):
            print("Student not found.")
            return

        if input(f"Delete student {student_id}? (y/N): ").strip().lower() != 'y':
            print("Cancelled.")
            return

        if self.student_service.delete_student(student_id):
            self.logger.info("Deleted student: %s", student_id)
            print("Student deleted successfully!")
        else:
            print("Student not found.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.view_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    try:
        config = load_config()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    setup_logging(config)
    app = StudentInformationSystem(StudentService(config['data_file']))
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    except Exception:
        logging.getLogger(__name__).exception("Unexpected error")
        print("Unexpected error. See the log file for details.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
