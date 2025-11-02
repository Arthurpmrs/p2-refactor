import datetime
import os
from builder import SchoolClassBuilder
from exceptions import InvalidMenuOptionException, UserCreationError
from factory import (
    EmployeeRegistrator,
    GuardianRegistrator,
    Registrator,
    StudentRegistrator,
)
from service import School
from system import ECA, Employee, SchoolClass, Student
from utils import select_multiple_options, read_non_empty_string, read_time


def input_school_class(teacher: Employee) -> SchoolClass:
    print("--- Cadastro de Turma ---")

    name = read_non_empty_string("Nome da turma")
    schedule = read_time()

    while True:
        try:
            n_classes_total = int(input("Número total de aulas previstas: ").strip())
            if n_classes_total <= 0:
                raise InvalidMenuOptionException()
            break
        except (ValueError, InvalidMenuOptionException):
            print("Opção inválida. O valor precisa ser um número maior que zero.")
            continue

    builder = SchoolClassBuilder()
    sclass = (
        builder.set_name(name)
        .set_teacher(teacher)
        .set_schedule(schedule)
        .set_n_classes_total(n_classes_total)
        .build()
    )

    print(f"\nTurma {sclass.name} criada com sucesso!")
    return sclass


def input_eca(teacher: Employee) -> ECA:
    print("--- Cadastro de Atividade Extracurricular ---")

    name = read_non_empty_string("Nome da atividade")
    schedule = read_time()

    eca = ECA(name=name, schedule=schedule, teacher=teacher)

    print(f"\nAtividade {eca.name} criada com sucesso!")
    return eca


def add_student_to_class(sclass: SchoolClass) -> list[Student]:
    school = School()
    print("--- Adicionar Alunos a uma Turma ---")

    students = school.get_alunos()
    sclass_student_ids = [s.id for s in sclass.students]
    students_not_in_class = [
        student for student in students if student.id not in sclass_student_ids
    ]

    if not students_not_in_class:
        print("Nenhum aluno disponível para matrícula.")
        return []

    print("\nAlunos disponíveis:")
    for i, student in enumerate(students_not_in_class, start=1):
        print(f"{i}. {student.name} (ID: {student.id})")

    selected_students = select_multiple_options(students_not_in_class)

    print(f"\n{len(selected_students)} aluno(s) adicionado(s) à turma '{sclass.name}'.")
    return selected_students


def add_student_to_eca(eca: ECA) -> list[Student]:
    school = School()
    print("--- Adicionar Alunos a uma Turma ---")

    students = school.get_alunos()
    eca_student_ids = [s.id for s in eca.students]
    students_not_in_eca = [
        student for student in students if student.id not in eca_student_ids
    ]

    if not students_not_in_eca:
        print("Nenhum aluno disponível.")
        return []

    print("\nAlunos disponíveis:")
    for i, student in enumerate(students_not_in_eca, start=1):
        print(f"{i}. {student.name} (ID: {student.id})")

    selected_students = select_multiple_options(students_not_in_eca)

    print(
        f"\n{len(selected_students)} aluno(s) adicionado(s) à atividade '{eca.name}'."
    )
    return selected_students


def visualizar_turma(sclass: SchoolClass):
    school = School()
    print("--- Informações da Turma ---")
    print(f"Nome: {sclass.name}")
    print(f"ID: {sclass.id}")
    print(f"Horário: {sclass.schedule.strftime('%H:%M')}")
    print(f"Aulas totais: {sclass.n_classes_total}")
    print(f"Aulas dadas: {sclass.n_classes_passed}")

    print("\nAlunos matriculados:")
    if sclass.students:
        for student in sclass.students:
            print(f"    {student.name} (ID: {student.id})")
    else:
        print("Nenhum aluno matriculado.")

    print("\nProvas:")
    exams = school.exam_repo.get_class_exams(sclass.id)
    if exams:
        for exam in exams:
            status = ""
            if exam.date > datetime.date.today():
                status = "prova agendada"
            elif not exam.grades_submitted:
                status = "notas não digitadas"
            else:
                status = "notas digitadas"

            print(f"    [{exam.date}] {exam.name} ({status})")
    else:
        print("Nenhuma prova cadastrada.")


def register_users():
    school = School()
    registrator: Registrator | None = None

    while True:
        os.system("clear")
        print("Selecione o tipo de usuário:")
        print("1 - Aluno")
        print("2 - Funcionário")
        print("3 - Responsável")

        tipo_opcao = input("\nEscolha uma opção: ")
        match tipo_opcao:
            case "1":
                registrator = StudentRegistrator()
            case "2":
                registrator = EmployeeRegistrator()
            case "3":
                registrator = GuardianRegistrator()
            case _:
                input("❌ Opção inválida. Clique Enter para voltar ao menu.")
                continue
        break

    try:
        user = registrator.create_user()
    except UserCreationError as e:
        print(str(e))
    else:
        school.register_user(user)
