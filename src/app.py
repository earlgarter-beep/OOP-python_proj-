import tkinter as tk
from tkinter import ttk, messagebox

from src.student import Student
from src.student_manager import StudentManager


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.manager = StudentManager()
        self.selected_student_id = None

        self.root.title("Student Management System")
        self.root.geometry("1050x650")
        self.root.minsize(850, 550)

        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Student Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        form = ttk.LabelFrame(self.root, text="Student Information", padding=12)
        form.pack(fill="x", padx=15, pady=5)

        self.entries = {}

        fields = [
            ("Student ID", "student_id"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Course", "course"),
            ("Year Level", "year_level"),
            ("Email", "email"),
        ]

        for index, (label_text, key) in enumerate(fields):
            row = index // 3
            column = (index % 3) * 2

            ttk.Label(form, text=label_text).grid(
                row=row, column=column, sticky="w", padx=5, pady=8
            )

            entry = ttk.Entry(form, width=25)
            entry.grid(
                row=row, column=column + 1, sticky="ew", padx=5, pady=8
            )

            self.entries[key] = entry

        for column in (1, 3, 5):
            form.columnconfigure(column, weight=1)

        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", padx=15, pady=10)

        ttk.Button(
            buttons, text="Add Student", command=self.add_student
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Update Selected", command=self.update_student
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Delete Selected", command=self.delete_student
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear Form", command=self.clear_form
        ).pack(side="left", padx=4)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_students())

        ttk.Button(
            search_frame, text="Search", command=self.search_students
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame, text="Show All", command=self.refresh_table
        ).pack(side="left", padx=4)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = (
            "student_id",
            "first_name",
            "last_name",
            "course",
            "year_level",
            "email",
        )

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )

        headings = {
            "student_id": "Student ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "course": "Course",
            "year_level": "Year",
            "email": "Email",
        }

        for column, heading in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=130, anchor="center")

        self.tree.column("email", width=200)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.select_student)

    def read_form(self):
        values = {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

        try:
            year_level = int(values["year_level"])
        except ValueError:
            raise ValueError("Year level must be a number.")

        return Student(
            student_id=values["student_id"],
            first_name=values["first_name"],
            last_name=values["last_name"],
            course=values["course"],
            year_level=year_level,
            email=values["email"],
        )

    def add_student(self):
        try:
            student = self.read_form()
            self.manager.add_student(student)

            messagebox.showinfo("Success", "Student added successfully.")
            self.clear_form()
            self.refresh_table()

        except (ValueError, TypeError) as error:
            messagebox.showerror("Error", str(error))
        except OSError as error:
            messagebox.showerror("File Error", str(error))

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning(
                "No Selection", "Select a student from the table first."
            )
            return

        try:
            student = self.read_form()

            self.manager.update_student(
                self.selected_student_id, student
            )

            messagebox.showinfo("Success", "Student updated successfully.")
            self.clear_form()
            self.refresh_table()

        except (ValueError, TypeError) as error:
            messagebox.showerror("Error", str(error))
        except OSError as error:
            messagebox.showerror("File Error", str(error))

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning(
                "No Selection", "Select a student from the table first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student {self.selected_student_id}?"
        )

        if not confirm:
            return

        try:
            self.manager.delete_student(self.selected_student_id)
            messagebox.showinfo("Success", "Student deleted successfully.")
            self.clear_form()
            self.refresh_table()

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def search_students(self):
        keyword = self.search_entry.get().strip()

        try:
            students = self.manager.search_students(keyword)
            self.display_students(students)
        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_table(self):
        try:
            students = self.manager.get_all_students()
            self.display_students(students)
        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def display_students(self, students):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student in students:
            self.tree.insert(
                "",
                "end",
                values=(
                    student.student_id,
                    student.first_name,
                    student.last_name,
                    student.course,
                    student.year_level,
                    student.email,
                ),
            )

    def select_student(self, event=None):
        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(selection[0], "values")
        self.selected_student_id = values[0]

        keys = [
            "student_id",
            "first_name",
            "last_name",
            "course",
            "year_level",
            "email",
        ]

        for key, value in zip(keys, values):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.selected_student_id = None

        for item in self.tree.selection():
            self.tree.selection_remove(item)


def run_app():
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()