import os

DATA_FILE="student.py"

class StudentManager:
    def __init__(self):
        self.students = {}
        self.load

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r")as f:
                    data = py.load(f)
                self.student =