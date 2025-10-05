import os

from service import School
from system import Employee, Guardian, Student
from menu import UserMenuContext
from menu.employee_menu import EmployeeMenuStrategy
from menu.guardian_menu import GuardianMenuStrategy
from menu.student_menu import StudentMenuStrategy


class App:
    school: School
    context: UserMenuContext

    def __init__(self):
        self.school = School()
        self.context = UserMenuContext()

    def start(self):
        while True:
            os.system("clear")
            print("=== 🎓 Sistema de Gestão Escolar ===\n")
            print("1 - Login")
            print("0 - Sair")
            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self.show_login_menu()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def show_login_menu(self):
        while True:
            os.system("clear")
            print("Selecione o tipo de usuário:")
            print("1 - Aluno")
            print("2 - Funcionário")
            print("3 - Responsável")
            print("0 - Voltar")
            tipo_opcao = input("\nEscolha uma opção: ")

            match tipo_opcao:
                case "1":
                    tipo = "aluno"
                case "2":
                    tipo = "funcionario"
                case "3":
                    tipo = "responsavel"
                case _:
                    print("❌ Opção inválida.")
                    input("Clique Enter para voltar ao menu.")
                    continue

            print(" ")
            nome = input("Nome: ")
            senha = input("Senha: ")
            usuario = self.school.login(nome, senha, tipo)

            if usuario is None:
                input("Clique Enter para tentar novamente.")
                continue

            print(f"\n✅ Login realizado como {usuario.get_type()}.")

            if isinstance(usuario, Student):
                strategy = StudentMenuStrategy(usuario)
            elif isinstance(usuario, Employee):
                strategy = EmployeeMenuStrategy(usuario)
            elif isinstance(usuario, Guardian):
                strategy = GuardianMenuStrategy(usuario)
            else:
                raise ValueError("User is not one of the known subclasses.")

            self.context.set_strategy(strategy)
            self.context.show_menu()

            break


if __name__ == "__main__":
    try:
        app = App()
        app.start()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
