from prompts import add_student_to_class, input_school_class, visualizar_turma
from system import Aluno, Funcionario, Responsavel
from service import Escola


# ========================
# Menus
# ========================
def menu_aluno(escola, aluno):
    print(f"\n🎓 Bem-vindo(a), {aluno.nome}!")
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Ver materiais")
        print("2. Ver notas")
        print("3. Ver provas agendadas")
        print("4. Ver presenças")
        print("5. Ver atividades extracurriculares")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                print(
                    "📚 Materiais:",
                    aluno.materiais
                    if aluno.materiais
                    else "📭 Nenhum material disponível.",
                )
            case "2":
                print(
                    "📊 Notas:",
                    aluno.notas if aluno.notas else "📉 Nenhuma nota registrada.",
                )
            case "3":
                print(
                    "📝 Provas:",
                    aluno.provas if aluno.provas else "📭 Nenhuma prova agendada.",
                )
            case "4":
                print(
                    f"✅ Presenças: {len(aluno.presencas)} dia(s)"
                    if aluno.presencas
                    else "❌ Nenhuma presença registrada."
                )
            case "5":
                print(
                    "🎯 Atividades:",
                    aluno.atividades
                    if aluno.atividades
                    else "📭 Nenhuma atividade registrada.",
                )
            case "0":
                break
            case _:
                print("Opção inválida.")


def menu_funcionario(escola: Escola, funcionario: Funcionario):
    print(f"\n👨‍🏫 Bem-vindo(a), {funcionario.nome} ({funcionario.cargo})!")
    while True:
        print("\n--- Menu do Funcionário ---")

        if funcionario.cargo in ["professor", "diretor"]:
            # professor e diretor têm todas as opções
            print(" 1. Registrar presença do aluno")
            print(" 2. Lançar nota do aluno")
            print(" 3. Distribuir material")
            print(" 4. Gerenciar turmas")
            print(" 5. Agendar prova")
            print(" 6. Registrar atividade extracurricular")
            print(" 7. Remover aluno")
            print(" 8. Consultar alunos matriculados")
            print(" 9. Rastrear transporte escolar")
            print("10. Adicioanr alunos a turmas")
            print("11. Visualizar turma")
            print("0. Sair")
        else:
            # motoristas e outros cargos: apenas presença e rastreamento
            print("1. Registrar presença do aluno")
            print("2. Rastrear transporte escolar")
            print("0. Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                try:
                    id_aluno = int(input("ID do aluno: "))
                    escola.registrar_presenca(id_aluno)
                except ValueError:
                    print("ID inválido.")
            case "2":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno: "))
                        nota = float(input("Nota a lançar: "))
                        disciplina = funcionario.disciplina
                        escola.lancar_nota(id_aluno, nota, disciplina)
                    except ValueError:
                        print("Valor inválido.")
                else:
                    try:
                        id_aluno = int(input("ID do aluno para rastrear transporte: "))
                        escola.rastrear_transporte(id_aluno)
                    except ValueError:
                        print("ID inválido.")
            case "3":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno: "))
                        material = input("Nome do material: ")
                        disciplina = funcionario.disciplina
                        escola.distribuir_material(id_aluno, material, disciplina)
                    except ValueError:
                        print("Valor inválido.")
                else:
                    print("Opção inválida.")
            case "4":
                if funcionario.cargo in ["professor", "diretor"]:
                    turma = input_school_class(funcionario)
                    escola.gerenciar_turmas(turma)
                else:
                    print("Opção inválida.")
            case "5":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno: "))
                        nome_prova = input("Nome da prova: ")
                        data_prova = input("Data da prova (DD/MM/AAAA): ")
                        disciplina = funcionario.disciplina
                        escola.agendar_prova(
                            id_aluno, nome_prova, data_prova, disciplina
                        )
                    except ValueError:
                        print("Valor inválido.")
                else:
                    print("Opção inválida.")
            case "6":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno: "))
                        atividade = input("Atividade extracurricular: ")
                        disciplina = funcionario.disciplina
                        escola.registrar_atividade(id_aluno, atividade, disciplina)
                    except ValueError:
                        print("ID inválido.")
                else:
                    print("Opção inválida.")
            case "7":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno para remoção: "))
                        escola.remover_aluno(id_aluno)
                    except ValueError:
                        print("ID inválido.")
                else:
                    print("Opção inválida.")
            case "8":
                if funcionario.cargo in ["professor", "diretor"]:
                    alunos = escola.consultar_alunos_matriculados()
                    if isinstance(alunos, str):
                        print(alunos)
                    else:
                        print("Alunos matriculados:")
                        for id_aluno, nome in alunos:
                            print(f"ID: {id_aluno} | Nome: {nome}")
                else:
                    print("Opção inválida.")
            case "9":
                if funcionario.cargo in ["professor", "diretor"]:
                    try:
                        id_aluno = int(input("ID do aluno para rastrear transporte: "))
                        escola.rastrear_transporte(id_aluno)
                    except ValueError:
                        print("ID inválido.")
                else:
                    print("Opção inválida.")
            case "10":
                if funcionario.cargo in ["professor", "diretor"]:
                    add_student_to_class(funcionario, escola)
            case "11":
                if funcionario.cargo in ["professor", "diretor"]:
                    visualizar_turma(funcionario, escola)
            case "0":
                break
            case _:
                print("Opção inválida.")


def menu_responsavel(escola, responsavel):
    print(f"\n👪 Bem-vindo, {responsavel.nome}!")
    while True:
        print("\n--- Menu do Responsável ---")
        print("1. Consultar dados do aluno")
        print("2. Pagar mensalidade")
        print("3. Rastrear transporte escolar")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                escola.consultar_dados_aluno(responsavel.id_aluno)
            case "2":
                print("💳 Formas de pagamento: PIX | Cartão | Boleto")
                forma_pagamento = input("Digite a forma de pagamento: ")
                escola.processar_pagamento(responsavel.id_aluno, forma_pagamento)
            case "3":
                escola.rastrear_transporte(responsavel.id_aluno)
            case "0":
                break
            case _:
                print("Opção inválida.")


# ========================
# Main
# ========================
def main():
    escola = Escola()
    print("\n=== 🎓 Sistema de Gestão Escolar ===")

    while True:
        print("\n1 - Login")
        print("2 - Cadastrar usuário")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        # ---------------- LOGIN ----------------
        if opcao == "1":
            print("\nSelecione o tipo de usuário:")
            print("1 - Aluno")
            print("2 - Funcionário")
            print("3 - Responsável")
            tipo_opcao = input("Escolha uma opção: ")

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
            usuario = escola.login(nome, senha, tipo)
            if usuario is None:
                continue
            print(f"\n✅ Login realizado como {usuario.exibir_tipo()}.")

            if isinstance(usuario, Aluno):
                menu_aluno(escola, usuario)
            elif isinstance(usuario, Funcionario):
                menu_funcionario(escola, usuario)
            elif isinstance(usuario, Responsavel):
                menu_responsavel(escola, usuario)

        # ---------------- CADASTRO ----------------
        elif opcao == "2":
            print("\nSelecione o tipo de usuário para cadastro:")
            print("1 - Aluno")
            print("2 - Funcionário")
            print("3 - Responsável")
            tipo_opcao = input("Escolha uma opção: ")

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
                cargo_opcao = input("Escolha uma opção: ")

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
                try:
                    id_aluno = int(
                        input("ID do aluno que o responsável irá acompanhar: ")
                    )
                except ValueError:
                    print("ID inválido.")
                    continue
                escola.cadastrar_usuario(tipo, nome, senha, id_aluno=id_aluno)

            else:
                escola.cadastrar_usuario(tipo, nome, senha)

        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
