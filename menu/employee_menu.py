from menu import UserMenuStrategy
from system import Employee, Exam, Resource
from utils import read_date, select_item
from input_helpers import (
    add_student_to_class,
    add_student_to_eca,
    input_eca,
    input_school_class,
    register_users,
    visualizar_turma,
)


class EmployeeMenuStrategy(UserMenuStrategy):
    employee: Employee

    def __init__(self, employee: Employee):
        self.employee = employee
        super().__init__()

    def set_menu_title(self):
        self.menu_title = (
            f"👨‍🏫 Bem-vindo(a), {self.employee.name} ({self.employee.position})!"
        )

    def set_logged_user(self):
        self.logged_user = self.employee

    def show_menu_options(self):
        if self.employee.position in {"professor", "diretor"}:
            print(" 1. Registrar presença")
            print(" 2. Lançar nota")
            print(" 3. Disponibilizar material para a turma")
            print(" 4. Agendar prova")
            print(" 5. Consultar alunos matriculados")
            print(" 6. Visualizar turmas")
            print(" 7. Criar turma")
            print(" 8. Adicionar alunos a turmas")
            print(" 9. Visualizar atividade extracurriculares")
            print("10. Criar atividade extracurricular")
            print("11. Adicionar alunos a atividades")
            print("12. Cadastrar usuários")
        else:
            print("1. Registrar presença")

    def match_option_to_function(self, selected_option: str) -> bool:
        match selected_option:
            case "1":
                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    sclass.n_classes_passed += 1
                    print("Registre a presença de cada aluno:")
                    for student in sclass.students:
                        while True:
                            resp = (
                                input(f"{student.name} presente (s/n)? ")
                                .strip()
                                .lower()
                            )
                            if resp == "s":
                                self.school.registrar_presenca(student, sclass)
                                break
                            elif resp == "n":
                                break
                            else:
                                print("    Inválido.")

                return False

            case "2":
                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    self.school.register_sclass_grades(sclass)

                return False

            case "3":
                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    name = input("Nome do material: ").strip()
                    url = input("Link do material: ")
                    resource = Resource(name, url)

                    self.school.distribuir_material(resource, sclass)

                return False

            case "4":
                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    print("Insira informações da prova: ")
                    name = input("Nome: ").strip()
                    date = read_date()
                    self.school.agendar_prova(sclass, Exam(sclass, name, date))

                return False

            case "5":
                print("👤 Veja todos os alunos matriculados:")
                for student in self.school.get_alunos():
                    print(f"{student.name} (ID: {student.id})")

                return True

            case "6":
                print("🏫 Ver detalhes de suas turmas:")

                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    visualizar_turma(sclass)

                return False

            case "7":
                sclass = input_school_class(self.employee)
                self.school.criar_turma(sclass)

                return True

            case "8":
                sclass = select_item(
                    self.school.get_sclass_from_teacher(self.employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    students = add_student_to_class(sclass)
                    self.school.add_students_to_sclass(sclass, students)

                return False

            case "9":
                ecas = self.school.eca_repo.get_ecas(self.employee.id)
                if ecas:
                    print("🎯 Ver as atividades extracurriculares que você gerencia:")
                    for eca in ecas:
                        print(f"[{eca.id}] {eca.name}")
                else:
                    print("Você não gerencia nenhuma atividade extracurricular.")

                return True

            case "10":
                eca = input_eca(self.employee)
                self.school.criar_atividade_extracurricular(eca)

                return True

            case "11":
                eca = select_item(
                    self.school.eca_repo.get_ecas(self.employee.id),
                    display_fn=lambda e: f"{e.name} (ID: {e.id})",
                    title="Selecione uma atividade extracurricular",
                )

                if eca:
                    students = add_student_to_eca(eca)
                    for student in students:
                        eca.students.append(student)

                return False

            case "12":
                register_users()

                return True

            case _:
                print("Opção inválida.")

        return True
