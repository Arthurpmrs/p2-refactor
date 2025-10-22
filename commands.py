from abc import ABC, abstractmethod

from menu.decorator import LogMenuDectorator
from service import School
from system import Employee, Guardian, Student, User
from menu import UserMenuContext, UserMenuStrategy
from menu.employee_menu import EmployeeMenuStrategy
from menu.guardian_menu import GuardianMenuStrategy
from menu.student_menu import StudentMenuStrategy


class LoginCommand(ABC):
    school: School
    user: User | None
    context: UserMenuContext

    def __init__(self, context: UserMenuContext):
        self.school = School()
        self.context = context

    def login(self):
        nome = input("\nNome: ")
        senha = input("Senha: ")
        self.user = self.school.login(nome, senha)

        if self.user is None:
            raise ValueError("Credenciais inválidas.")

        print(f"\n✅ Login realizado como {self.user.get_type()}.")

    def execute(self):
        self.login()
        self.context.set_strategy(self.get_correct_strategy())

    @abstractmethod
    def get_correct_strategy(self) -> UserMenuStrategy:
        pass


class LoginAsStudentCommand(LoginCommand):
    def get_correct_strategy(self):
        if not self.user or not isinstance(self.user, Student):
            raise ValueError("User of wrong type")

        return LogMenuDectorator(StudentMenuStrategy(self.user))


class LoginAsEmpoloyeeCommand(LoginCommand):
    def get_correct_strategy(self):
        if not self.user or not isinstance(self.user, Employee):
            raise ValueError("User of wrong type")

        return LogMenuDectorator(EmployeeMenuStrategy(self.user))


class LoginAsGuardianCommand(LoginCommand):
    def get_correct_strategy(self):
        if not self.user or not isinstance(self.user, Guardian):
            raise ValueError("User of wrong type")

        return LogMenuDectorator(GuardianMenuStrategy(self.user))
