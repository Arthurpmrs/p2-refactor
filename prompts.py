from datetime import time
from system import Escola, Funcionario, SchoolClass


def input_school_class(teacher: Funcionario) -> SchoolClass:
    """
    Cria uma nova SchoolClass a partir da entrada do usuário.
    :param next_id: ID que será atribuído automaticamente à turma.
    :return: instância de SchoolClass
    """
    print("\n--- Cadastro de Turma ---")

    name = input("Nome da turma: ").strip()

    # Captura horário no formato HH:MM
    while True:
        horario_str = input("Horário da turma (HH:MM): ").strip()
        try:
            hora, minuto = map(int, horario_str.split(":"))
            horario = time(hora, minuto)
            break
        except Exception:
            print("Formato inválido! Use HH:MM, por exemplo 14:30.")

    while True:
        try:
            n_classes_total = int(input("Número total de aulas previstas: ").strip())
            if n_classes_total < 0:
                raise ValueError
            break
        except ValueError:
            print("Digite um número inteiro válido e não negativo.")

    # Criar objeto
    turma = SchoolClass(
        name=name,
        time=horario,
        teacher=teacher,
        n_classes_total=n_classes_total,
        n_classes_passed=0,
    )

    print("\nTurma criada com sucesso!")
    return turma


def add_student_to_class(teacher: Funcionario, school: Escola):
    """
    Permite escolher uma turma de um professor e adicionar alunos a ela.
    """
    print("\n--- Adicionar Alunos a uma Turma ---")

    # 1. Listar turmas do professor
    turmas = school.sclass_repo.get_teacher_classes(teacher.id)
    if not turmas:
        print("Este professor não possui turmas cadastradas.")
        return

    print("\nTurmas disponíveis:")
    for i, turma in enumerate(turmas, start=1):
        print(f"{i}. {turma.name} (ID: {turma.id})")

    # 2. Selecionar turma
    while True:
        try:
            escolha = int(input("Selecione o número da turma: ").strip())
            if 1 <= escolha <= len(turmas):
                turma_escolhida = turmas[escolha - 1]
                break
            else:
                print("Opção inválida, tente novamente.")
        except ValueError:
            print("Digite um número válido.")

    # 3. Listar alunos disponíveis
    alunos = school.get_alunos()
    if not alunos:
        print("Nenhum aluno disponível para matrícula.")
        return

    print("\nAlunos disponíveis:")
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno.nome} (ID: {aluno.id})")

    # 4. Selecionar múltiplos alunos
    print("Digite os números dos alunos separados por vírgula (ex: 1,3,5):")
    while True:
        entrada = input("Seleção: ").strip()
        try:
            indices = [int(x) for x in entrada.split(",") if x.strip()]
            if not indices:
                raise ValueError
            if all(1 <= idx <= len(alunos) for idx in indices):
                alunos_escolhidos = [alunos[idx - 1] for idx in indices]
                break
            else:
                print("Algum número está fora da lista. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Use números separados por vírgula.")

    # Adicionar alunos à turma
    for aluno in alunos_escolhidos:
        if aluno not in turma_escolhida.students:
            turma_escolhida.students.append(aluno)

    print(
        f"\n{len(alunos_escolhidos)} aluno(s) adicionado(s) à turma '{turma_escolhida.name}'."
    )


def visualizar_turma(teacher: Funcionario, school: Escola):
    """
    Permite selecionar uma turma de um professor e visualizar suas informações básicas.
    """
    print("\n--- Visualizar Turma ---")

    # 1. Listar turmas do professor
    turmas = school.sclass_repo.get_teacher_classes(teacher.id)
    if not turmas:
        print("Este professor não possui turmas cadastradas.")
        return

    print("\nTurmas disponíveis:")
    for i, turma in enumerate(turmas, start=1):
        print(f"{i}. {turma.name} (ID: {turma.id})")

    # 2. Selecionar turma
    while True:
        try:
            escolha = int(input("Selecione o número da turma: ").strip())
            if 1 <= escolha <= len(turmas):
                turma_escolhida = turmas[escolha - 1]
                break
            else:
                print("Opção inválida, tente novamente.")
        except ValueError:
            print("Digite um número válido.")

    # 3. Mostrar informações básicas
    print("\n--- Informações da Turma ---")
    print(f"Nome: {turma_escolhida.name}")
    print(f"ID: {turma_escolhida.id}")
    print(
        f"Horário: {turma_escolhida.time.strftime('%H:%M') if turma_escolhida.time else 'Não definido'}"
    )
    print(f"Aulas totais: {turma_escolhida.n_classes_total}")
    print(f"Aulas dadas: {turma_escolhida.n_classes_passed}")

    # Alunos
    print("\nAlunos matriculados:")
    if turma_escolhida.students:
        for aluno in turma_escolhida.students:
            print(f"- {aluno.nome} (ID: {aluno.id})")
    else:
        print("Nenhum aluno matriculado.")

    # Provas
    print("\nProvas:")
    if turma_escolhida.exams:
        for exam in turma_escolhida.exams:
            print(f"- {exam.title} em {exam.date}")
    else:
        print("Nenhuma prova cadastrada.")
