from src.student import Student
from src.student_repository import StudentRepository


class StudentManager:
    def __init__(self, repository=None):
        self.repository = repository or StudentRepository()

    def get_all_students(self):
        return self.repository.get_all()

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Expected a Student object.")

        students = self.get_all_students()

        if any(
            item.student_id.lower() == student.student_id.lower()
            for item in students
        ):
            raise ValueError("Student ID already exists.")

        students.append(student)
        self.repository.save_all(students)

    def find_student(self, student_id):
        student_id = student_id.strip()

        for student in self.get_all_students():
            if student.student_id.lower() == student_id.lower():
                return student

        return None

    def search_students(self, keyword):
        keyword = keyword.strip().lower()

        if not keyword:
            return self.get_all_students()

        results = []

        for student in self.get_all_students():
            searchable_fields = [
                student.student_id,
                student.first_name,
                student.last_name,
                student.full_name,
                student.course,
                student.email,
                str(student.year_level),
            ]

            if any(keyword in value.lower() for value in searchable_fields):
                results.append(student)

        return results

    def update_student(self, student_id, updated_student):
        if not isinstance(updated_student, Student):
            raise TypeError("Expected a Student object.")

        students = self.get_all_students()

        for index, student in enumerate(students):
            if student.student_id.lower() == student_id.strip().lower():

                if (
                    updated_student.student_id.lower()
                    != student.student_id.lower()
                    and any(
                        item.student_id.lower()
                        == updated_student.student_id.lower()
                        for item in students
                    )
                ):
                    raise ValueError("Student ID already exists.")

                students[index] = updated_student
                self.repository.save_all(students)
                return

        raise ValueError("Student not found.")

    def delete_student(self, student_id):
        students = self.get_all_students()

        remaining_students = [
            student
            for student in students
            if student.student_id.lower() != student_id.strip().lower()
        ]

        if len(remaining_students) == len(students):
            raise ValueError("Student not found.")

        self.repository.save_all(remaining_students)