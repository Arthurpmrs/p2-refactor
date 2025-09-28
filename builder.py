import datetime
from system import Employee, Resource, SchoolClass, Student


class SchoolClassBuilder:
    def __init__(self):
        self._name: str | None = None
        self._teacher: Employee | None = None
        self._schedule: datetime.time | None = None
        self._students: list[Student] = []
        self._resources: list[Resource] = []
        self._n_classes_total: int = 0
        self._n_classes_passed: int = 0

    def set_name(self, name: str) -> "SchoolClassBuilder":
        self._name = name
        return self

    def set_teacher(self, teacher: Employee) -> "SchoolClassBuilder":
        self._teacher = teacher
        return self

    def set_schedule(self, schedule: datetime.time) -> "SchoolClassBuilder":
        self._schedule = schedule
        return self

    def add_student(self, student: Student) -> "SchoolClassBuilder":
        self._students.append(student)
        return self

    def add_resource(self, resource: Resource) -> "SchoolClassBuilder":
        self._resources.append(resource)
        return self

    def set_n_classes_total(self, total: int) -> "SchoolClassBuilder":
        self._n_classes_total = total
        return self

    def set_n_classes_passed(self, passed: int) -> "SchoolClassBuilder":
        self._n_classes_passed = passed
        return self

    def build(self) -> SchoolClass:
        if not self._name or not self._teacher or not self._schedule:
            raise ValueError("Turma requer nome, professor e horário")

        return SchoolClass(
            name=self._name,
            teacher=self._teacher,
            schedule=self._schedule,
            students=self._students,
            resources=self._resources,
            n_classes_total=self._n_classes_total,
            n_classes_passed=self._n_classes_passed,
        )


class EmployeeBuilder:
    def __init__(self):
        self._name = None
        self._password = None
        self._position = None
        self._subject = None

    def set_name(self, name: str):
        self._name = name
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def as_professor(self, subject: str):
        self._position = "professor"
        self._subject = subject
        return self

    def as_director(self):
        self._position = "diretor"
        self._subject = None
        return self

    def as_staff(self, position: str):
        """Para outros cargos administrativos"""
        self._position = position
        self._subject = None
        return self

    def build(self) -> Employee:
        if not self._name or not self._password or not self._position:
            raise ValueError(
                "Nome, senha e posição são obrigatórios para criar um Employee"
            )
        return Employee(
            name=self._name,
            password=self._password,
            position=self._position,
            subject=self._subject,
        )
