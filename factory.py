from abc import ABC, abstractmethod

from builder import EmployeeBuilder
from exceptions import UserCreationError
from service import School
from system import Guardian, Student, User
from utils import read_non_empty_string, select_item


class Registrator(ABC):
    @abstractmethod
    def create_user(self) -> User:
        pass


class StudentRegistrator(Registrator):
    def create_user(self) -> User:
        print("--- Cadastro de Aluno ---")

        student_name = read_non_empty_string("Nome do aluno")
        student_password = read_non_empty_string("Senha do aluno")

        return Student(name=student_name, password=student_password)


class GuardianRegistrator(Registrator):
    def create_user(self) -> User:
        print("--- Cadastro de Responsável ---")
        guardian_name = read_non_empty_string("Nome do responsável")
        guardian_password = read_non_empty_string("Senha do responsável")

        school = School()
        student = select_item(
            school.get_alunos(),
            display_fn=lambda s: f"{s.name} (ID: {s.id})",
            title="Selecione um estudante",
        )

        if student is None:
            raise UserCreationError(
                "É necessário selecionar um aluno para cadastrar um responsável."
            )

        return Guardian(name=guardian_name, password=guardian_password, student=student)


class EmployeeRegistrator(Registrator):
    POSITIONS: set[str] = {"professor", "diretor", "motorista", "zelador"}

    def create_user(self) -> User:
        print("--- Cadastro de Funcionário ---")
        builder = EmployeeBuilder()
        employee_name = read_non_empty_string("Nome do funcionário")
        employee_password = read_non_empty_string("Senha do funcionário")

        builder = builder.set_name(employee_name).set_password(employee_password)

        while True:
            employee_position = read_non_empty_string("Cargo do funcionário")

            if employee_position.lower() in EmployeeRegistrator.POSITIONS:
                break

            print("Esse cargo não é permitido! Insira um dos seguintes valores")
            print(", ".join([p.title() for p in EmployeeRegistrator.POSITIONS]))

        if employee_position == "professor":
            employee_subject = read_non_empty_string("Matéria do professor")
            builder = builder.as_professor(employee_subject)
        elif employee_position == "diretor":
            builder = builder.as_director()
        else:
            builder = builder.as_staff(employee_position)

        return builder.build()
