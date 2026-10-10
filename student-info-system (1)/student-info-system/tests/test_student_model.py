import unittest

from models.student import Student

VALID = dict(name=" Grace Hopper ", email=" Grace@Navy.mil ", course="Computing", year_level="3")


class StudentModelTests(unittest.TestCase):
    def test_generates_id_and_normalizes(self):
        s = Student(**VALID)
        self.assertEqual(len(s.student_id), 8)
        self.assertEqual((s.name, s.email, s.year_level, s.gpa), ("Grace Hopper", "grace@navy.mil", 3, 0.0))

    def test_keeps_given_id(self):
        self.assertEqual(Student(student_id="S-9", **VALID).student_id, "S-9")

    def test_to_dict_has_all_fields(self):
        keys = {'student_id', 'name', 'email', 'course', 'year_level', 'gpa', 'created_at', 'updated_at'}
        self.assertEqual(set(Student(**VALID).to_dict()), keys)

    def test_invalid_values_raise(self):
        bad_inputs = [{"name": " "}, {"email": "nope"}, {"course": ""}, {"year_level": "abc"},
                      {"year_level": 9}, {"gpa": 5}, {"gpa": "x"}]
        for bad in bad_inputs:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Student(**{**VALID, **bad})


if __name__ == "__main__":
    unittest.main()
