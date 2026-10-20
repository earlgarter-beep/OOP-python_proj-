import os
import tempfile
import unittest
from unittest.mock import patch

from src.student import Student
from src.student_manager import StudentManager


def make_student(student_id="S001", first_name="Ada", last_name="Lovelace"):
    return Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        course="Computing",
        year_level=2,
        email=f"{first_name.lower()}@example.com",
    )


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.database_file = os.path.join(self.temp_dir.name, "database.py")
        self.data_file_patch = patch(
            "src.student_manager.DATA_FILE", self.database_file
        )
        self.data_file_patch.start()
        self.addCleanup(self.data_file_patch.stop)
        self.manager = StudentManager()

    def test_add_student_is_persisted_and_reloaded(self):
        student = make_student()

        self.manager.add_student(student)
        reloaded = StudentManager()

        self.assertEqual(reloaded.get_all_students(), [student])

    def test_duplicate_student_id_is_rejected(self):
        self.manager.add_student(make_student())

        with self.assertRaisesRegex(ValueError, "already exists"):
            self.manager.add_student(make_student(first_name="Grace"))

        self.assertEqual(len(self.manager.get_all_students()), 1)

    def test_update_and_delete(self):
        self.manager.add_student(make_student())
        updated = make_student(first_name="Augusta")

        self.manager.update_student("S001", updated)
        self.assertEqual(self.manager.get_all_students(), [updated])

        self.manager.delete_student("S001")
        self.assertEqual(self.manager.get_all_students(), [])

    def test_search_matches_student_fields_case_insensitively(self):
        student = make_student()
        self.manager.add_student(student)

        self.assertEqual(self.manager.search_students("LOVELACE"), [student])
        self.assertEqual(self.manager.search_students("example.com"), [student])
        self.assertEqual(self.manager.search_students("missing"), [])


if __name__ == "__main__":
    unittest.main()