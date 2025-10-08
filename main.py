import os

from commands import (
    LoginAsEmpoloyeeCommand,
    LoginAsGuardianCommand,
    LoginAsStudentCommand,
)
from service import School
from menu import UserMenuContext


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
            option = input("\nEscolha uma opção: ")

            match option:
                case "1":
                    command = LoginAsStudentCommand(self.context)
                case "2":
                    command = LoginAsEmpoloyeeCommand(self.context)
                case "3":
                    command = LoginAsGuardianCommand(self.context)
                case _:
                    print("❌ Opção inválida.")
                    input("Clique Enter para voltar ao menu.")
                    continue

            command.execute()
            self.context.show_menu()

            break


if __name__ == "__main__":
    try:
        app = App()
        app.start()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
