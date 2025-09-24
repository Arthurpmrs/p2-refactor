from repository import (
    AttendanceRepository,
    ExamRepository,
    SchoolClassRepository,
    UserRepository,
)
from system import Employee, Exam, Guardian, Resource, SchoolClass, Student, User


class School:
    def __init__(self):
        self.students = []
        self.funcionarios = []
        self.responsaveis = []
        self.turmas = []
        self.proximo_id = 1
        self.sclass_repo = SchoolClassRepository()
        self.user_repo = UserRepository()
        self.attendance_repo = AttendanceRepository()
        self.exam_repo = ExamRepository()

        # -------------------
        # Banco de exemplos
        # -------------------
        # Criando alunos
        aluno1 = Student("João", "123")
        self.user_repo.add_user(aluno1)

        aluno2 = Student("Maria", "123")
        self.user_repo.add_user(aluno2)

        # Criando professor
        prof = Employee("Carlos", "123", "professor", "Matemática")
        self.user_repo.add_user(prof)

        # Criando diretor
        diretor = Employee("Fernanda", "123", "diretor")
        self.user_repo.add_user(diretor)

        # Criando motorista
        motorista = Employee("José", "123", "motorista")
        self.user_repo.add_user(motorista)

        # Criando responsável (ligado ao aluno João)
        responsavel = Guardian("Ana", "123", aluno1)
        self.user_repo.add_user(responsavel)

    def cadastrar_usuario(
        self,
        tipo: str,
        nome: str,
        senha: str,
        cargo: str | None = None,
        disciplina: str | None = None,
        student: Student | None = None,
    ):
        if tipo == "aluno":
            aluno = Student(nome, senha)
            self.user_repo.add_user(aluno)
            print(f"Aluno {nome} cadastrado com ID {self.proximo_id}")

        elif tipo == "funcionario" and cargo is not None:
            funcionario = Employee("Carlos", "123", "professor", "Matemática")
            funcionario = Employee(nome, senha, cargo, disciplina)
            self.user_repo.add_user(funcionario)

            if cargo == "professor":
                print(
                    f"Professor {nome} de {disciplina} cadastrado (ID {self.proximo_id})"
                )
            elif cargo == "diretor":
                print(f"Diretor {nome} cadastrado (ID {self.proximo_id})")
            else:
                print(
                    f"Funcionário {nome} cadastrado como {cargo} (ID {self.proximo_id})"
                )

        elif tipo == "responsavel" and student is not None:
            responsavel = Guardian(nome, senha, student)
            self.user_repo.add_user(responsavel)
            print(f"Responsável {nome} cadastrado com ID {self.proximo_id}")
        else:
            print("Tipo inválido para cadastro.")
            return

    def login(self, nome: str, senha: str, tipo: str) -> User | None:
        try:
            return self.user_repo.validate_user(nome, senha)
        except ValueError:
            print("Credenciais Inválidas!\n")
            return None

    def registrar_presenca(self, student: Student, sclass: SchoolClass):
        at = self.attendance_repo.register_attendance(student, sclass)
        print(f"Presença registrada para {student.name} em {at.date}")

    def lancar_nota(self, exam: Exam, student: Student, grade: float):
        self.exam_repo.register_grade(exam, student, grade)
        print(
            f"Nota {grade} lançada para {student.name} na prova {exam.name} da turma {exam.sclass.name}"
        )

    def distribuir_material(self, resource: Resource, sclass: SchoolClass):
        self.sclass_repo.add_resource(sclass.id, resource)
        print(f"Material '{resource.name}' disponível para turma {sclass.name}")

    def agendar_prova(self, sclass: SchoolClass, exam: Exam):
        self.exam_repo.create_exam(sclass, exam)
        print(
            f"Prova '{exam.name}' agendada para a turma {sclass.name} na data {exam.date}"
        )

    def registrar_atividade(self, id_aluno, atividade, disciplina):
        aluno = next((a for a in self.students if a.id == id_aluno), None)
        if aluno:
            aluno.atividades.append({"atividade": atividade, "disciplina": disciplina})
            print(
                f"Atividade '{atividade}' de {disciplina} registrada para {aluno.nome}"
            )
        else:
            print("Aluno não encontrado.")

    def consultar_dados_aluno(self, id_aluno):
        aluno = next((a for a in self.students if a.id == id_aluno), None)
        if aluno:
            print(f"\n📋 Dados do aluno {aluno.nome}:")
            print(
                "📚 Materiais:",
                aluno.materiais
                if aluno.materiais
                else "📭 Nenhum material disponível.",
            )
            print(
                "📈 Notas:",
                aluno.notas if aluno.notas else "📉 Nenhuma nota registrada.",
            )
            print(
                "📅 Provas:",
                aluno.provas if aluno.provas else "📭 Nenhuma prova agendada.",
            )
            print(
                f"✅ Presenças: {len(aluno.presencas)} dia(s)"
                if aluno.presencas
                else "❌ Nenhuma presença registrada."
            )
            print(
                "🎯 Atividades:",
                aluno.atividades
                if aluno.atividades
                else "📭 Nenhuma atividade registrada.",
            )
        else:
            print("Aluno não encontrado.")

    def processar_pagamento(self, id_aluno, forma_pagamento):
        aluno = next((a for a in self.students if a.id == id_aluno), None)
        if aluno:
            print(
                f"✅ Pagamento da mensalidade de {aluno.nome} realizado via {forma_pagamento}."
            )
        else:
            print("Aluno não encontrado.")

    def rastrear_transporte(self, id_aluno):
        aluno = next((a for a in self.students if a.id == id_aluno), None)
        if aluno:
            print(
                f"🛰️ Rastreamento do transporte escolar de {aluno.nome} em andamento..."
            )
        else:
            print("Aluno não encontrado.")

    def remover_aluno(self, id_aluno):
        aluno = next((a for a in self.students if a.id == id_aluno), None)
        if aluno:
            self.students.remove(aluno)
            print(f"🗑️ Aluno {aluno.nome} removido com sucesso.")
        else:
            print("Aluno não encontrado.")

    def consultar_alunos_matriculados(self):
        if not self.students:
            return "Nenhum aluno matriculado."
        return [(aluno.id, aluno.nome) for aluno in self.students]

    def gerenciar_turmas(self, sclass: SchoolClass):
        self.turma_repo.criar_turma(sclass)
        print(f"🧑‍🏫 Turma '{sclass.name}' criada no horário {sclass.time}")

    def get_alunos(self) -> list[Aluno]:
        return self.students
