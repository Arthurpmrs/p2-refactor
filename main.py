import os
from system import Employee, Exam, Guardian, PaymentMethod, Resource, Student
from service import School
from utils import (
    read_date,
    select_item,
)
from input_helpers import (
    add_student_to_class,
    add_student_to_eca,
    input_eca,
    input_school_class,
    register_student_and_guardian,
    visualizar_turma,
)


def menu_aluno(school: School, student: Student):
    while True:
        os.system("clear")
        print(f"🎓 Bem-vindo(a), {student.name}!")

        print("\n--- Menu do Aluno ---")
        print("1. Ver turmas")
        print("2. Ver materiais")
        print("3. Ver provas e notas")
        print("4. Ver presenças")
        print("5. Ver atividades extracurriculares")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")
        os.system("clear")
        match opcao:
            case "1":
                school.consultar_turmas(student)
            case "2":
                school.consultar_materiais(student)
            case "3":
                school.consultar_notas_e_provas(student)
            case "4":
                school.consultar_presencas(student)
            case "5":
                school.consultar_ecas(student)
            case "0":
                break
            case _:
                print("Opção inválida.")

        input("\nClique Enter para voltar ao menu.")


def menu_funcionario(school: School, employee: Employee):
    while True:
        os.system("clear")
        print(f"👨‍🏫 Bem-vindo(a), {employee.name} ({employee.position})!")

        print("\n--- Menu do Funcionário ---")
        if employee.position in {"professor", "diretor"}:
            # professor e diretor têm todas as opções
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
            print("12. Matricular aluno")
            print(" 0. Sair")
        else:
            # motoristas e outros cargos: apenas presença e rastreamento
            print("1. Registrar presença")
            print("0. Sair")

        opcao = input("\nEscolha uma opção: ")
        os.system("clear")
        match opcao:
            case "1":
                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
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
                                school.registrar_presenca(student, sclass)
                                break
                            elif resp == "n":
                                break
                            else:
                                print("    Inválido.")

            case "2":
                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    school.register_sclass_grades(sclass)

            case "3":
                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    name = input("Nome do material: ").strip()
                    url = input("Link do material: ")
                    resource = Resource(name, url)

                    school.distribuir_material(resource, sclass)

            case "4":
                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    print("Insira informações da prova: ")
                    name = input("Nome: ").strip()
                    date = read_date()
                    school.agendar_prova(sclass, Exam(sclass, name, date))

            case "5":
                print("👤 Veja todos os alunos matriculados:")
                for student in school.get_alunos():
                    print(f"{student.name} (ID: {student.id})")

            case "6":
                print("🏫 Ver detalhes de suas turmas:")

                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    visualizar_turma(sclass, school)

            case "7":
                sclass = input_school_class(employee)
                school.criar_turma(sclass)

            case "8":
                sclass = select_item(
                    school.get_sclass_from_teacher(employee),
                    display_fn=lambda c: f"{c.name} (ID: {c.id})",
                    title="Selecione uma turma",
                )

                if sclass is not None:
                    students = add_student_to_class(sclass, school)
                    school.add_students_to_sclass(sclass, students)

            case "9":
                ecas = school.eca_repo.get_ecas(employee.id)
                if ecas:
                    print("🎯 Ver as atividades extracurriculares que você gerencia:")
                    for eca in ecas:
                        print(f"[{eca.id}] {eca.name}")
                else:
                    print("Você não gerencia nenhuma atividade extracurricular.")

            case "10":
                eca = input_eca(employee)
                school.criar_atividade_extracurricular(eca)

            case "11":
                eca = select_item(
                    school.eca_repo.get_ecas(employee.id),
                    display_fn=lambda e: f"{e.name} (ID: {e.id})",
                    title="Selecione uma atividade extracurricular",
                )
                if eca:
                    students = add_student_to_eca(eca, school)
                    for student in students:
                        eca.students.append(student)

            case "12":
                register_student_and_guardian(school)

            case "0":
                break

            case _:
                print("Opção inválida.")

        input("\nClique Enter para voltar ao menu.")


def menu_responsavel(school: School, guardian: Guardian):
    while True:
        os.system("clear")
        print(f"👪 Bem-vindo, {guardian.name}!")

        print("\n--- Menu do Responsável ---")
        print("1. Consultar dados do aluno")
        print("2. Pagar mensalidade")
        print("3. Rastrear transporte escolar")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")
        os.system("clear")
        match opcao:
            case "1":
                school.consultar_dados_aluno(guardian.student)
            case "2":
                print("💳 Formas de pagamento: PIX | Cartão | Boleto")
                forma_pagamento = input("Digite a forma de pagamento: ")
                try:
                    payment_method = PaymentMethod[forma_pagamento.upper()]
                    school.processar_pagamento(guardian.student, payment_method)
                except Exception:
                    print("Opção inválida.")
            case "3":
                school.rastrear_transporte(guardian.student)
            case "0":
                break
            case _:
                print("Opção inválida.")

        input("\nClique Enter para voltar ao menu.")


def main():
    escola = School()

    while True:
        os.system("clear")
        print("=== 🎓 Sistema de Gestão Escolar ===")
        print("\n1 - Login")
        # print("2 - Cadastrar usuário")
        print("0 - Sair")
        opcao = input("\nEscolha uma opção: ")

        # ---------------- LOGIN ----------------
        if opcao == "1":
            os.system("clear")
            print("Selecione o tipo de usuário:")
            print("1 - Aluno")
            print("2 - Funcionário")
            print("3 - Responsável")
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
            usuario = escola.login(nome, senha, tipo)

            if usuario is None:
                input("Clique Enter para tentar novamente.")
                continue

            print(f"\n✅ Login realizado como {usuario.show_type()}.")

            if isinstance(usuario, Student):
                menu_aluno(escola, usuario)
            elif isinstance(usuario, Employee):
                menu_funcionario(escola, usuario)
            elif isinstance(usuario, Guardian):
                menu_responsavel(escola, usuario)

        # ---------------- CADASTRO ----------------
        elif opcao == "2.":
            print("\nSelecione o tipo de usuário para cadastro:")
            print("1 - Aluno")
            print("2 - Funcionário")
            print("3 - Responsável")
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
                    continue

            nome = input("Nome: ")
            senha = input("Senha: ")

            if tipo == "funcionario":
                print("\nSelecione o cargo:")
                print("1 - Diretor")
                print("2 - Professor")
                print("3 - Motorista")
                print("4 - Outro")
                cargo_opcao = input("\nEscolha uma opção: ")

                match cargo_opcao:
                    case "1":
                        cargo = "diretor"
                        disciplina = input(
                            "Digite a disciplina que o diretor irá acompanhar (ou deixe vazio): "
                        )
                        if disciplina.strip() == "":
                            disciplina = None
                    case "2":
                        cargo = "professor"
                        disciplina = input(
                            "Digite a disciplina que o professor irá lecionar: "
                        )
                    case "3":
                        cargo = "motorista"
                        disciplina = None
                    case "4":
                        cargo = input("Digite o nome do cargo: ")
                        disciplina = None
                    case _:
                        print("❌ Opção inválida.")
                        continue

                escola.cadastrar_usuario(
                    tipo, nome, senha, cargo=cargo, disciplina=disciplina
                )

            elif tipo == "responsavel":
                student = select_item(
                    escola.get_alunos(),
                    display_fn=lambda s: f"{s.name} (ID: {s.id})",
                    title="Selecione o aluno",
                )

                escola.cadastrar_usuario(tipo, nome, senha, student=student)

            else:
                escola.cadastrar_usuario(tipo, nome, senha)

        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
