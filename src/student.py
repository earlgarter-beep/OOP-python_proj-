from dataclasses import asdict, dataclass


@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    course: str
    year_level: int
    email: str

    def __post_init__(self):
        text_fields = (
            "student_id",
            "first_name",
            "last_name",
            "course",
            "email",
        )
        for field in text_fields:
            value = getattr(self, field)
            if not isinstance(value, str):
                raise ValueError(f"{field.replace('_', ' ').title()} must be text.")
            value = value.strip()
            if not value:
                raise ValueError("All fields must be provided and cannot be empty.")
            setattr(self, field, value)

        if isinstance(self.year_level, str):
            try:
                self.year_level = int(self.year_level.strip())
            except ValueError as error:
                raise ValueError("Year level must be a number.") from error
        elif isinstance(self.year_level, bool) or not isinstance(self.year_level, int):
            raise ValueError("Year level must be a number.")

        if not 1 <= self.year_level <= 5:
            raise ValueError("Year level must be between 1 and 5.")

        if "@" not in self.email or "." not in self.email.rsplit("@", 1)[-1]:
            raise ValueError("Invalid email address format.")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
