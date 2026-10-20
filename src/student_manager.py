import os
import importlib.util
import pprint

from student import Student


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.py")


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number.")


def ask_email(prompt):
    while True:
        email = input(prompt).strip()
        if "@" in email and "." in email.split("@")[-1]:
            return email
        print("Please enter a valid email (e.g. name@example.com).")


class StudentManager:
    def __init__(self):
        self.students = {}
        self.load()

    def load(self):
        if not os.path.exists(DATA_FILE):
            self.save()
            return
        try:
            spec = importlib.util.spec_from_file_location("database", DATA_FILE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.students = {
                s["student_id"]: Student.from_dict(s) for s in module.STUDENTS
            }
        except Exception as e:
            print(f"Warning: could not read database.py ({e})")

    def save(self):
        data = [s.to_dict() for s in self.students.values()]
        with open(DATA_FILE, "w") as f:
            f.write("# Auto-generated student database. Edit with care.\n")
            f.write("STUDENTS = ")
            f.write(pprint.pformat(data, sort_dicts=False))
            f.write("\n")

    def add(self, student):
        if student.student_id in self.students:
            print("A student with that ID already exists.")
            return
        self.students[student.student_id] = student
        self.save()
        print("Student added.")

    def view_all(self):
        if not self.students:
            print("No students found.")
            return
        header = (
            f"{'ID':<8}{'Name':<20}{'Age':<6}{'Course':<18}"
            f"{'Year':<6}{'Email':<28}"
        )
        print(header)
        print("-" * len(header))
        for s in sorted(self.students.values(), key=lambda s: s.name.lower()):
            print(s)

    def search(self, keyword):
        keyword = keyword.lower()
        result = [
            s for s in self.students.values()
            if keyword in s.name.lower()
            or keyword == s.student_id.lower()
            or keyword == s.email.lower()
        ]
        if not result:
            print("Not found.")
            return
        for s in result:
            print(s)

    def update(self, student_id):
        s = self.students.get(student_id)
        if not s:
            print("Not found!")
            return
        print("Leave a field blank to keep the current value.")
        s.name = input(f"Name [{s.name}]: ").strip() or s.name

        age = input(f"Age [{s.age}]: ").strip()
        s.age = int(age) if age.isdigit() else s.age

        s.course = input(f"Course [{s.course}]: ").strip() or s.course

        year = input(f"Year level [{s.year_level}]: ").strip()
        s.year_level = int(year) if year.isdigit() else s.year_level

        email = input(f"Email [{s.email}]: ").strip()
        if email:
            if "@" in email and "." in email.split("@")[-1]:
                s.email = email
            else:
                print("Invalid email, keeping the old one.")

        self.save()
        print("Student updated.")

    def delete(self, student_id):
        if self.students.pop(student_id, None):
            self.save()
            print("Student deleted.")
        else:
            print("Student not found.")

    def stats(self):
        if not self.students:
            print("No data yet.")
            return
        ages = [s.age for s in self.students.values()]
        print(f"Total students : {len(ages)}")
        print(f"Average age    : {sum(ages) / len(ages):.1f}")
        print("Students per year level:")
        counts = {}
        for s in self.students.values():
            counts[s.year_level] = counts.get(s.year_level, 0) + 1
        for year in sorted(counts):
            print(f"  Year {year}: {counts[year]}")


def main():
    manager = StudentManager()
    menu = """
=== Student ===
1. Add student
2. View all students
3. Search student
4. Update student
5. Delete student
6. Statistics
0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            sid = input("ID: ").strip()
            name = input("Name: ").strip()
            age = ask_int("Age: ")
            course = input("Course: ").strip()
            year_level = ask_int("Year level: ")
            email = ask_email("Email: ")
            manager.add(Student(sid, name, age, course, year_level, email))
        elif choice == "2":
            manager.view_all()
        elif choice == "3":
            manager.search(input("Enter name, ID or email: ").strip())
        elif choice == "4":
            manager.update(input("Enter student ID: ").strip())
        elif choice == "5":
            manager.delete(input("Enter student ID: ").strip())
        elif choice == "6":
            manager.stats()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid input, try again.")


if __name__ == "__main__":
    main()
