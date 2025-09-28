import datetime
from builder import SchoolClassBuilder
from service import School
from system import ECA, Employee, Guardian, SchoolClass, Student
from utils import read_time


def input_school_class(teacher: Employee) -> SchoolClass:
    print("--- Cadastro de Turma ---")

    name = input("Nome da turma: ").strip()
    schedule = read_time()

    while True:
        try:
            n_classes_total = int(input("Número total de aulas previstas: ").strip())
            if n_classes_total < 0:
                raise ValueError
            break
        except ValueError:
            print("Digite um número inteiro válido e não negativo.")

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

    name = input("Nome da atividade: ").strip()
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

    print("Digite os números dos alunos separados por vírgula (ex: 1,3,5):")
    while True:
        entrada = input("Seleção: ").strip()
        try:
            indices = [int(x) for x in entrada.split(",") if x.strip()]
            if not indices:
                raise ValueError
            if all(1 <= idx <= len(students_not_in_class) for idx in indices):
                selected_students = [students_not_in_class[idx - 1] for idx in indices]
                break
            else:
                print("Algum número está fora da lista. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Use números separados por vírgula.")

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

    print("Digite os números dos alunos separados por vírgula (ex: 1,3,5):")
    while True:
        entrada = input("Seleção: ").strip()
        try:
            indices = [int(x) for x in entrada.split(",") if x.strip()]
            if not indices:
                raise ValueError
            if all(1 <= idx <= len(students_not_in_eca) for idx in indices):
                selected_students = [students_not_in_eca[idx - 1] for idx in indices]
                break
            else:
                print("Algum número está fora da lista. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Use números separados por vírgula.")

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


def register_student_and_guardian():
    school = School()

    print("--- Cadastro de Aluno ---")
    nome_aluno = input("Nome do aluno: ").strip()
    senha_aluno = input("Senha do aluno: ").strip()

    aluno = Student(name=nome_aluno, password=senha_aluno)
    school.user_repo.add_user(aluno)

    print("\n--- Cadastro de Responsável ---")
    nome_resp = input("Nome do responsável: ").strip()
    senha_resp = input("Senha do responsável: ").strip()

    resp = Guardian(name=nome_resp, password=senha_resp, student=aluno)
    school.user_repo.add_user(resp)

    print(f"\n✅ Matrícula de {aluno.name} realizada com sucesso!")
