from menu import UserMenuStrategy
from system import Student


class StudentMenuStrategy(UserMenuStrategy):
    student: Student

    def __init__(self, student: Student):
        super().__init__()
        self.student = student
        self.menu_title = f"🎓 Bem-vindo(a), {self.student.name}!"

    def show_menu_options(self):
        print("\n--- Menu do Aluno ---")
        print("1. Ver turmas")
        print("2. Ver materiais")
        print("3. Ver provas e notas")
        print("4. Ver presenças")
        print("5. Ver atividades extracurriculares")

    def match_option_to_function(self, selected_option: str) -> bool:
        match selected_option:
            case "1":
                self.school.consultar_turmas(self.student)
            case "2":
                self.school.consultar_materiais(self.student)
            case "3":
                self.school.consultar_notas_e_provas(self.student)
            case "4":
                self.school.consultar_presencas(self.student)
            case "5":
                self.school.consultar_ecas(self.student)
            case _:
                print("Opção inválida.")

        return True
