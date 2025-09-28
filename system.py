import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum


class PaymentMethod(StrEnum):
    PIX = "PIX"
    CREDIT_CARD = "Cartão de Crédito"
    BOLETO = "Boleto"


@dataclass
class User(ABC):
    id: int = field(init=False)
    name: str
    password: str

    def validate_password(self, password: str):
        return self.password == password

    @abstractmethod
    def get_type(self) -> str:
        pass


@dataclass
class Employee(User):
    position: str
    subject: str | None = None

    def get_type(self) -> str:
        if self.position == "professor":
            return f"Funcionário ({self.position} de {self.subject})"
        elif self.position == "diretor":
            return "Funcionário (diretor)"
        return f"Funcionário ({self.position})"


@dataclass
class Student(User):
    def get_type(self):
        return "Aluno"


@dataclass
class Guardian(User):
    student: Student

    def get_type(self) -> str:
        return "Responsável"


@dataclass
class Resource:
    name: str
    url: str


@dataclass
class Activity(ABC):
    id: int = field(init=False)
    name: str
    teacher: Employee
    schedule: datetime.time
    students: list[Student] = field(default_factory=list[Student])

    def get_schedule(self) -> str:
        return self.schedule.strftime("%H:%M")


@dataclass
class SchoolClass(Activity):
    resources: list[Resource] = field(default_factory=list[Resource])
    n_classes_total: int = 0
    n_classes_passed: int = 0


@dataclass
class ECA(Activity):
    pass


@dataclass
class Exam:
    id: int = field(init=False)
    sclass: SchoolClass
    name: str
    date: datetime.date
    grades_submitted: bool = False


@dataclass
class StudentExamResult:
    student: Student
    exam: Exam
    grade: float | None = None


@dataclass
class Attendance:
    student: Student
    sclass: SchoolClass
    date: datetime.date = field(default_factory=datetime.date.today)
