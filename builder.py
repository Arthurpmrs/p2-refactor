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
