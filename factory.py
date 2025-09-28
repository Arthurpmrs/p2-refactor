from abc import ABC, abstractmethod

from builder import EmployeeBuilder
from service import School
from system import Guardian, Student, User
from utils import select_item


class Registrator(ABC):
    @abstractmethod
    def create_user(self) -> User:
        pass


class StudentRegistrator(Registrator):
    def create_user(self) -> User:
        print("--- Cadastro de Aluno ---")
        student_name = input("Nome do aluno: ").strip()
        student_password = input("Senha do aluno: ").strip()

        return Student(name=student_name, password=student_password)


class GuardianRegistrator(Registrator):
    def create_user(self) -> User:
        print("--- Cadastro de Responsável ---")
        guardian_name = input("Nome do responsável: ").strip()
        guardian_password = input("Senha do responsável: ").strip()

        school = School()
        student = select_item(
            school.get_alunos(),
            display_fn=lambda s: f"{s.name} (ID: {s.id})",
            title="Selecione um estudante",
        )

        if student is None:
            raise ValueError(
                "É necessário selecionar um aluno para cadastrar um responsável."
            )

        return Guardian(name=guardian_name, password=guardian_password, student=student)


class EmployeeRegistrator(Registrator):
    POSITIONS: set[str] = {"professor", "diretor", "motorista", "zelador"}

    def create_user(self) -> User:
        print("--- Cadastro de Funcionário ---")
        builder = EmployeeBuilder()
        employee_name = input("Nome do funcionário: ").strip()
        employee_password = input("Senha do funcionário: ").strip()

        builder = builder.set_name(employee_name).set_password(employee_password)

        while True:
            employee_position = input("Cargo do funcionário: ").strip().lower()

            if employee_position in EmployeeRegistrator.POSITIONS:
                break

            print("Esse cargo não é permitido! Insira um cargo válido.")

        if employee_position == "professor":
            employee_subject = input("Matéria do professor: ").strip()
            builder = builder.as_professor(employee_subject)
        elif employee_position == "diretor":
            builder = builder.as_director()
        else:
            builder = builder.as_staff(employee_position)

        return builder.build()
