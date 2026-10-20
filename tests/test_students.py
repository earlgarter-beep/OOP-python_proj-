import unittest

from src.student import Student


class StudentTests(unittest.TestCase):
    def test_normalizes_fields_and_round_trips(self):
        student = Student(
            student_id=" S001 ",
            first_name=" Ada ",
            last_name=" Lovelace ",
            course=" Computing ",
            year_level="2",
            email=" ada@example.com ",
        )

        self.assertEqual(student.full_name, "Ada Lovelace")
        self.assertEqual(student.year_level, 2)
        self.assertEqual(Student.from_dict(student.to_dict()), student)

    def test_rejects_year_levels_outside_supported_range(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 5"):
            Student(
                student_id="S001",
                first_name="Ada",
                last_name="Lovelace",
                course="Computing",
                year_level=6,
                email="ada@example.com",
            )


if __name__ == "__main__":
    unittest.main()