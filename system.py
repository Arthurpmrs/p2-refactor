import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class User(ABC):
    id: int = field(init=False)
    name: str
    password: str

    def validate_password(self, password: str):
        return self.password == password

    @abstractmethod
    def show_type(self) -> str:
        pass


@dataclass
class Employee(User):
    position: str
    subject: str | None = None

    def show_type(self) -> str:
        if self.position == "professor":
            return f"Funcionário ({self.position} de {self.subject})"
        elif self.position == "diretor":
            return "Funcionário (diretor)"
        return f"Funcionário ({self.position})"


@dataclass
class Student(User):
    def show_type(self):
        return "Aluno"


@dataclass
class Guardian(User):
    student: Student

    def show_type(self) -> str:
        return "Responsável"


@dataclass
class Resource:
    name: str
    url: str


@dataclass
class SchoolClass:
    id: int = field(init=False)
    name: str
    teacher: Employee
    schedule: tuple[datetime.time, list[int]]
    resources: list[Resource] = field(default_factory=list[Resource])
    students: list[Student] = field(default_factory=list[Student])
    n_classes_total: int = 0
    n_classes_passed: int = 0


@dataclass
class Exam:
    id: int = field(init=False)
    sclass: SchoolClass
    name: str
    date: datetime.date


@dataclass
class StudentExamResult:
    id: int = field(init=False)
    student: Student
    exam: Exam
    grade: float | None = None


@dataclass
class Attendance:
    student: Student
    sclass: SchoolClass
    date: datetime.date = field(default_factory=datetime.date.today)
