from itertools import count
from typing import Iterator

from system import (
    ECA,
    Attendance,
    Resource,
    SchoolClass,
    Exam,
    Student,
    StudentExamResult,
    User,
)


class UserRepository:
    __users: dict[int, User]
    __id_counter: Iterator[int]

    def __init__(self):
        self.__users = {}
        self.__id_counter = count(1)

    def add_user(self, user: User) -> int:
        user_id = next(self.__id_counter)
        user.id = user_id
        self.__users.update({user_id: user})
        return user_id

    def validate_user(self, name: str, password: str) -> User:
        selected_user = None
        for user in self.__users.values():
            if user.name == name:
                selected_user = user
                break

        if not selected_user:
            raise ValueError("Credenciais inválidas.")

        if selected_user.password != password:
            raise ValueError("Credenciais inválidas.")

        return selected_user


class SchoolClassRepository:
    __classes: dict[int, SchoolClass]
    __id_counter: Iterator[int]

    def __init__(self):
        self.__classes = {}
        self.__id_counter = count(1)

    def create_sclass(self, sclass: SchoolClass) -> int:
        sclass_id = next(self.__id_counter)
        sclass.id = sclass_id
        self.__classes.update({sclass_id: sclass})
        return sclass_id

    def get_teacher_sclasses(self, teacher_id: int) -> list[SchoolClass]:
        return [
            sclass
            for sclass in self.__classes.values()
            if sclass.teacher.id == teacher_id
        ]

    def add_resource(self, sclass_id: int, resource: Resource):
        self.__classes[sclass_id].resources.append(resource)

    def get_student_sclasses(self, student_id: int) -> list[SchoolClass]:
        return [
            sclass
            for sclass in self.__classes.values()
            if student_id in [s.id for s in sclass.students]
        ]


class ExamRepository:
    __exams: dict[int, Exam]
    __id_counter: Iterator[int]
    __exam_results: dict[tuple[int, int], StudentExamResult]

    def __init__(self):
        self.__exams = {}
        self.__exam_results = {}
        self.__id_counter = count(1)

    def create_exam(self, sclass: SchoolClass, exam: Exam) -> int:
        exam_id = next(self.__id_counter)
        exam.id = exam_id
        self.__exams.update({exam_id: exam})

        for student in sclass.students:
            self.__exam_results.update(
                {(exam_id, student.id): StudentExamResult(student=student, exam=exam)}
            )

        return exam_id

    def register_grade(self, exam: Exam, student: Student, grade: float):
        exam_result = self.__exam_results.get((exam.id, student.id))

        if not exam_result:
            raise ValueError("Aluno não está cadastrado na prova.")

        exam_result.grade = grade

    def get_class_exams(self, sclass_id: int) -> list[Exam]:
        return [exam for exam in self.__exams.values() if exam.sclass.id == sclass_id]

    def get_student_exam_results(self, student_id: int) -> list[StudentExamResult]:
        return [
            student_exam
            for student_exam in self.__exam_results.values()
            if student_exam.student.id == student_id
        ]

    def get_student_exam_result_in_class(
        self, student_id: int, sclass_id: int
    ) -> list[StudentExamResult]:
        return [
            student_exam
            for student_exam in self.__exam_results.values()
            if (
                student_exam.student.id == student_id
                and student_exam.exam.sclass.id == sclass_id
            )
        ]

    def get_students_exams(self, exam_id: int) -> list[StudentExamResult]:
        return [
            student_exam
            for student_exam in self.__exam_results.values()
            if student_exam.exam.id == exam_id
        ]


class AttendanceRepository:
    __attendance: list[Attendance]

    def __init__(self):
        self.__attendance = []

    def register_attendance(self, student: Student, sclass: SchoolClass) -> Attendance:
        at = Attendance(student, sclass)
        self.__attendance.append(at)
        return at

    def get_student_attendance_for_class(
        self, student: Student, sclass: SchoolClass
    ) -> float:
        student_ats = [
            at
            for at in self.__attendance
            if at.student.id == student.id and at.sclass.id == sclass.id
        ]
        return len(student_ats) / sclass.n_classes_passed

    def get_student_attendances(
        self, student: Student
    ) -> list[tuple[SchoolClass, float]]:
        at_by_class: dict[int, list[Attendance]] = {}
        sclasses: dict[int, SchoolClass] = {}
        for at in self.__attendance:
            if at.student.id != student.id:
                continue

            if at.sclass.id in at_by_class:
                at_by_class[at.sclass.id].append(at)
                sclasses.update({at.sclass.id: at.sclass})
            else:
                at_by_class.update({at.sclass.id: [at]})

        result: list[tuple[SchoolClass, float]] = []
        for idx, ats in at_by_class.items():
            sclass = sclasses.get(idx)

            if not sclass:
                raise ValueError("Algum deu errado")

            percentage = len(ats) / sclass.n_classes_passed
            result.append((sclass, percentage))

        return result


class ECARepository:
    __ecas: dict[int, ECA]
    __id_counter: Iterator[int]

    def __init__(self):
        self.__ecas = {}
        self.__id_counter = count(1)

    def create_eca(self, eca: ECA) -> int:
        eca_id = next(self.__id_counter)
        eca.id = eca_id
        self.__ecas.update({eca_id: eca})
        return eca_id

    def get_ecas(self, teacher_id: int) -> list[ECA]:
        return [eca for eca in self.__ecas.values() if eca.teacher.id == teacher_id]

    def get_student_ecas(self, student_id: int) -> list[ECA]:
        return [
            eca
            for eca in self.__ecas.values()
            if student_id in [s.id for s in eca.students]
        ]
