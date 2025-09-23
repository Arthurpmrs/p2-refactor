from datetime import datetime
from abc import ABC, abstractmethod

# ========================
# Classe Base (Abstrata)
# ========================
class Usuario(ABC):
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self._senha = senha  # encapsulamento

    def validar_senha(self, senha):
        return self._senha == senha

    @abstractmethod
    def exibir_tipo(self):
        pass

# ========================
# Subclasses
# ========================
class Aluno(Usuario):
    def __init__(self, id, nome, senha):
        super().__init__(id, nome, senha)
        self.presencas = []
        self.notas = []
        self.materiais = []
        self.atividades = []
        self.provas = []

    def exibir_tipo(self):
        return "Aluno"

class Funcionario(Usuario):
    def __init__(self, id, nome, senha, cargo, disciplina=None):
        super().__init__(id, nome, senha)
        self.cargo = cargo.lower()
        self.disciplina = disciplina

    def exibir_tipo(self):
        if self.cargo == "professor":
            return f"Funcionário ({self.cargo} de {self.disciplina})"
        elif self.cargo == "diretor":
            return "Funcionário (diretor)"
        return f"Funcionário ({self.cargo})"

class Responsavel(Usuario):
    def __init__(self, id, nome, senha, id_aluno):
        super().__init__(id, nome, senha)
        self.id_aluno = id_aluno

    def exibir_tipo(self):
        return "Responsável"

# ========================
# Classe Escola
# ========================
class Escola:
    def __init__(self):
        self.alunos = []
        self.funcionarios = []
        self.responsaveis = []
        self.turmas = []
        self.proximo_id = 1

        # -------------------
        # Banco de exemplos
        # -------------------
        # Criando alunos
        aluno1 = Aluno(self.proximo_id, "João", "123")
        self.alunos.append(aluno1)
        self.proximo_id += 1

        aluno2 = Aluno(self.proximo_id, "Maria", "123")
        self.alunos.append(aluno2)
        self.proximo_id += 1

        # Criando professor
        prof = Funcionario(self.proximo_id, "Carlos", "123", "professor", "Matemática")
        self.funcionarios.append(prof)
        self.proximo_id += 1

        # Criando diretor
        diretor = Funcionario(self.proximo_id, "Fernanda", "123", "diretor")
        self.funcionarios.append(diretor)
        self.proximo_id += 1

        # Criando motorista
        motorista = Funcionario(self.proximo_id, "José", "123", "motorista")
        self.funcionarios.append(motorista)
        self.proximo_id += 1

        # Criando responsável (ligado ao aluno João)
        responsavel = Responsavel(self.proximo_id, "Ana", "123", aluno1.id)
        self.responsaveis.append(responsavel)
        self.proximo_id += 1

    # ----------------------
    # Cadastro
    # ----------------------
    def cadastrar_usuario(self, tipo, nome, senha, id_aluno=None, cargo=None, disciplina=None):
        if tipo == "aluno":
            aluno = Aluno(self.proximo_id, nome, senha)
            self.alunos.append(aluno)
            print(f"Aluno {nome} cadastrado com ID {self.proximo_id}")

        elif tipo == "funcionario":
            funcionario = Funcionario(self.proximo_id, nome, senha, cargo, disciplina)
            self.funcionarios.append(funcionario)
            if cargo == "professor":
                print(f"Professor {nome} de {disciplina} cadastrado (ID {self.proximo_id})")
            elif cargo == "diretor":
                print(f"Diretor {nome} cadastrado (ID {self.proximo_id})")
            else:
                print(f"Funcionário {nome} cadastrado como {cargo} (ID {self.proximo_id})")

        elif tipo == "responsavel":
            if not any(a.id == id_aluno for a in self.alunos):
                print("ID de aluno inválido para o responsável.")
                return
            responsavel = Responsavel(self.proximo_id, nome, senha, id_aluno)
            self.responsaveis.append(responsavel)
            print(f"Responsável {nome} cadastrado com ID {self.proximo_id}")

        else:
            print("Tipo inválido para cadastro.")
            return

        self.proximo_id += 1

    # ----------------------
    # Login
    # ----------------------
    def login(self, nome, senha, tipo):
        if tipo == "aluno":
            lista = self.alunos
        elif tipo == "funcionario":
            lista = self.funcionarios
        elif tipo == "responsavel":
            lista = self.responsaveis
        else:
            print("❌ Tipo inválido.")
            return None

        for usuario in lista:
            if usuario.nome == nome and usuario.validar_senha(senha):
                return usuario

        print("❌ Nome ou senha inválidos. Tente novamente.")
        return None

    # ----------------------
    # Funcionalidades
    # ----------------------
    def registrar_presenca(self, id_aluno):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            data = datetime.now()
            aluno.presencas.append(data)
            print(f"Presença registrada para {aluno.nome} em {data.strftime('%d/%m/%Y')}")
        else:
            print("Aluno não encontrado.")

    def lancar_nota(self, id_aluno, nota, disciplina):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            aluno.notas.append({"nota": nota, "disciplina": disciplina})
            print(f"Nota {nota} lançada para {aluno.nome} em {disciplina}")
        else:
            print("Aluno não encontrado.")

    def distribuir_material(self, id_aluno, material, disciplina):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            aluno.materiais.append({"material": material, "disciplina": disciplina})
            print(f"Material '{material}' de {disciplina} distribuído para {aluno.nome}")
        else:
            print("Aluno não encontrado.")

    def agendar_prova(self, id_aluno, nome_prova, data_prova, disciplina):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            aluno.provas.append({"nome": nome_prova, "data": data_prova, "disciplina": disciplina})
            print(f"Prova '{nome_prova}' de {disciplina} agendada para {aluno.nome} na data {data_prova}")
        else:
            print("Aluno não encontrado.")

    def registrar_atividade(self, id_aluno, atividade, disciplina):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            aluno.atividades.append({"atividade": atividade, "disciplina": disciplina})
            print(f"Atividade '{atividade}' de {disciplina} registrada para {aluno.nome}")
        else:
            print("Aluno não encontrado.")

    def consultar_dados_aluno(self, id_aluno):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            print(f"\n📋 Dados do aluno {aluno.nome}:")
            print("📚 Materiais:", aluno.materiais if aluno.materiais else "📭 Nenhum material disponível.")
            print("📈 Notas:", aluno.notas if aluno.notas else "📉 Nenhuma nota registrada.")
            print("📅 Provas:", aluno.provas if aluno.provas else "📭 Nenhuma prova agendada.")
            print(f"✅ Presenças: {len(aluno.presencas)} dia(s)" if aluno.presencas else "❌ Nenhuma presença registrada.")
            print("🎯 Atividades:", aluno.atividades if aluno.atividades else "📭 Nenhuma atividade registrada.")
        else:
            print("Aluno não encontrado.")

    def processar_pagamento(self, id_aluno, forma_pagamento):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            print(f"✅ Pagamento da mensalidade de {aluno.nome} realizado via {forma_pagamento}.")
        else:
            print("Aluno não encontrado.")

    def rastrear_transporte(self, id_aluno):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            print(f"🛰️ Rastreamento do transporte escolar de {aluno.nome} em andamento...")
        else:
            print("Aluno não encontrado.")

    def remover_aluno(self, id_aluno):
        aluno = next((a for a in self.alunos if a.id == id_aluno), None)
        if aluno:
            self.alunos.remove(aluno)
            print(f"🗑️ Aluno {aluno.nome} removido com sucesso.")
        else:
            print("Aluno não encontrado.")

    def consultar_alunos_matriculados(self):
        if not self.alunos:
            return "Nenhum aluno matriculado."
        return [(aluno.id, aluno.nome) for aluno in self.alunos]

    def gerenciar_turmas(self, nome_turma, horario):
        self.turmas.append({"nome": nome_turma, "horario": horario})
        print(f"🧑‍🏫 Turma '{nome_turma}' criada no horário {horario}")
