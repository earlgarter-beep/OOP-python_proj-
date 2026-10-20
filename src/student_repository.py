import json
from pathlib import Path

from src.student import Student


class StudentRepository:
    def __init__(self, file_path=None):
        if file_path is None:
            project_root = Path(__file__).resolve().parent.parent
            file_path = project_root / "data" / "students.json"

        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def get_all(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Student data file contains invalid JSON: {error}"
            ) from error

        if not isinstance(data, list):
            raise ValueError("Student data must be a JSON list.")

        return [Student.from_dict(item) for item in data]

    def save_all(self, students):
        data = [student.to_dict() for student in students]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_by_id(self, student_id):
        for student in self.get_all():
            if student.student_id == student_id:
                return student

        return None