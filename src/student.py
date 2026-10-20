from dataclasses import dataclass, asdict

@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    course: str
    year_level: str
    email: str

    def __post_init__(self):
        self.student_id = self.student_id.strip()
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.course = self.course.strip()
        self.year_level = self.year_level.strip()
        self.email = self.email.strip()

        if not all([self.student_id,
                     self.first_name, 
                     self.last_name, 
                     self.course, 
                     self.year_level, 
                     self.email]):
            raise ValueError("All fields must be provided and cannot be empty.")
        
        if isinstance(self.year_level, str) and not self.year_level.isdigit():
            raise ValueError("Year level must be a number!")

        if self.year_level not in range (1, 6):
            raise ValueError("Year level must be between 1 and 5.")

        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email address format.")

        @property
        def full_name(self):
            return f"{self.first_name} {self.last_name}"

        def to_dict(self):
            return asdict(self)

        @classmethod 
        def from_dict(cls, data):
            return cls(**data)