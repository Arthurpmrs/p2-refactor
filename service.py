import datetime
from repository import (
    AttendanceRepository,
    ECARepository,
    ExamRepository,
    SchoolClassRepository,
    UserRepository,
)
from system import (
    ECA,
    Employee,
    Exam,
    Guardian,
    PaymentMethod,
    Resource,
    SchoolClass,
    Student,
    User,
)
from utils import generate_random_hash, select_item


class School:
    __instance = None
    _initialized = False

    def __new__(cls):
        if School.__instance is None:
            School.__instance = super().__new__(cls)
            School.__instance._initialized = False
        return School.__instance

    def __init__(self):
        if not self._initialized:
            self.sclass_repo = SchoolClassRepository()
            self.user_repo = UserRepository()
            self.attendance_repo = AttendanceRepository()
            self.exam_repo = ExamRepository()
            self.eca_repo = ECARepository()

            self.populate()

            self._initialized = True

    def register_user(self, user: User):
        idx = self.user_repo.add_user(user)
        print(f"{user.get_type()} cadastrado (ID {idx})")

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

    def criar_atividade_extracurricular(self, eca: ECA):
        self.eca_repo.create_eca(eca)
        print(
            f"Atividade Extracurricular '{eca.name}' criada pelo funcionário {eca.teacher.name}"
        )

    def consultar_dados_aluno(self, student: Student):
        student_sclasses = self.sclass_repo.get_student_sclasses(student.id)
        print(f"📋 Dados do(a) aluno(a) {student.name}:")
        if not student_sclasses:
            print("\n📭 O(A) aluno(a) não foi cadastrado(a) em uma turma.")

        for sclass in student_sclasses:
            print(f"\n🏫 Turma {sclass.name} ({sclass.get_schedule()})")

            print("    📚 Materiais:")
            if sclass.resources:
                for resource in sclass.resources:
                    print(f"        {resource.name} ({resource.url})")
            else:
                print("        📭 Nenhum material disponível.")

            exam_results = self.exam_repo.get_student_exam_result_in_class(
                student.id, sclass.id
            )
            print("    📈 Provas e Notas:")
            if exam_results:
                sorted_result = sorted(exam_results, key=lambda r: r.exam.date)
                for result in sorted_result:
                    status = ""
                    if result.exam.date > datetime.date.today():
                        status = "prova agendada"
                    elif result.grade is None:
                        status = "nota não registrada"
                    elif result.grade:
                        status = f"nota {result.grade}"

                    print(f"        [{result.exam.date}] {result.exam.name} ({status})")
            else:
                print("        📭 Nenhum prova ou nota disponível.")

            ats = self.attendance_repo.get_student_attendance_for_class(student, sclass)
            print("    📅 Presenças:")
            if ats is not None:
                print(
                    f"        ✅ Presença (%): {(ats * 100):.2f} (registradas {sclass.n_classes_passed} aulas)"
                )
            else:
                print("        📭 Nenhuma presença registrada para essa turma.")

        student_ecas = self.eca_repo.get_student_ecas(student.id)
        print("\n🎯 Atividades extracurriculares:")
        if student_ecas:
            for eca in student_ecas:
                print(f"   {eca.name} ({eca.get_schedule()})")
        else:
            print("    📭 O aluno não participa de nenhuma atividade extracurricular.")

    def consultar_materiais(self, student: Student):
        student_sclasses = self.sclass_repo.get_student_sclasses(student.id)

        print("📚 Materiais:")
        if not student_sclasses:
            print("    📭 O(A) não foi cadastrado(a) em uma turma.")

        for sclass in student_sclasses:
            print(f"🏫 Turma {sclass.name} ({sclass.get_schedule()})")
            if sclass.resources:
                for resource in sclass.resources:
                    print(f"    {resource.name} ({resource.url})")
            else:
                print("    📭 Nenhum material disponível.")

    def consultar_notas_e_provas(self, student: Student):
        student_sclasses = self.sclass_repo.get_student_sclasses(student.id)

        print("📈 Provas e Notas:")
        if not student_sclasses:
            print("    📭 O(A) não foi cadastrado(a) em uma turma.")

        for sclass in student_sclasses:
            print(f"🏫 Turma {sclass.name} ({sclass.get_schedule()})")

            exam_results = self.exam_repo.get_student_exam_result_in_class(
                student.id, sclass.id
            )
            if exam_results:
                sorted_result = sorted(exam_results, key=lambda r: r.exam.date)
                for result in sorted_result:
                    status = ""
                    if result.exam.date > datetime.date.today():
                        status = "prova agendada"
                    elif result.grade is None:
                        status = "nota não registrada"
                    elif result.grade:
                        status = f"nota {result.grade}"

                    print(f"        [{result.exam.date}] {result.exam.name} ({status})")
            else:
                print("    📭 Nenhum prova ou nota disponível.")

    def consultar_presencas(self, student: Student):
        student_sclasses = self.sclass_repo.get_student_sclasses(student.id)

        print("📅 Presenças:")
        if not student_sclasses:
            print("    📭 O(A) não foi cadastrado(a) em uma turma.")

        for sclass in student_sclasses:
            print(f"🏫 Turma {sclass.name} ({sclass.get_schedule()})")

            ats = self.attendance_repo.get_student_attendance_for_class(student, sclass)
            if ats is not None:
                print(
                    f"    ✅ Presença (%): {(ats * 100):.2f} (registradas {sclass.n_classes_passed} aulas)"
                )
            else:
                print("    📭 Nenhuma presença registrada para essa turma.")

    def consultar_ecas(self, student: Student):
        student_ecas = self.eca_repo.get_student_ecas(student.id)
        print("🎯 Atividades extracurriculares:")
        if student_ecas:
            for eca in student_ecas:
                print(f"   {eca.name} ({eca.get_schedule()})")
        else:
            print("    📭 O aluno não participa de nenhuma atividade extracurricular.")

    def consultar_turmas(self, student: Student):
        student_sclasses = self.sclass_repo.get_student_sclasses(student.id)

        print("🏫 Turmas:")
        for sclass in student_sclasses:
            print(f"    {sclass.name} ({sclass.get_schedule()})")

    def processar_pagamento(self, student: Student, method: PaymentMethod):
        if method == PaymentMethod.BOLETO:
            print(
                f"\n✅ Boleto gerado para {student.name}. Clique no link abaixo para visualizar:"
            )
            print(
                f"🔗 www.payment.school.com.br/{student.id}/pdf/{generate_random_hash()}"
            )
        else:
            print(
                f"\n⏳ Clique no link abaixo para concluir o pagamento da mensalidade de {student.name}."
            )
            print(f"🔗 www.payment.school.com.br/{student.id}/{generate_random_hash()}")

    def rastrear_transporte(self, student: Student):
        print(
            f"🛰️ Transporte de {student.name} em andamento. Clique no link para acompanhar: "
        )
        print(f"🔗 www.transport.school.com.br/{student.id}/{generate_random_hash()}")

    def criar_turma(self, sclass: SchoolClass):
        self.sclass_repo.create_sclass(sclass)
        print(f"🧑‍🏫 Turma '{sclass.name}' criada no horário {sclass.get_schedule()}")

    def get_alunos(self) -> list[Student]:
        return self.user_repo.get_students()

    def get_sclass_from_teacher(self, teacher: Employee):
        return self.sclass_repo.get_teacher_sclasses(teacher.id)

    def register_sclass_grades(self, sclass: SchoolClass):
        exam = select_item(
            self.exam_repo.get_class_exams_without_grade(sclass.id),
            display_fn=lambda e: f"{e.name} (DATA: {e.date})",
            title="Selecione uma prova da turma",
        )

        if exam:
            exam.grades_submitted = True
            print(f"Registre a nota dos alunos na prova {exam.name}:")
            for student in sclass.students:
                while True:
                    resp = input(f"Nota de {student.name}? ").strip().lower()
                    try:
                        grade = float(resp)
                        self.lancar_nota(exam, student, grade)
                        break
                    except Exception:
                        print("    Inválido.")

    def add_students_to_sclass(self, sclass: SchoolClass, students: list[Student]):
        for student in students:
            sclass.students.append(student)

            # Cria provas para novo aluno
            for exam in self.exam_repo.get_class_exams(sclass.id):
                if exam.grades_submitted:
                    grade = 10.0
                else:
                    grade = None

                self.exam_repo.register_grade(exam, student, grade, force=True)

            for _ in range(sclass.n_classes_passed):
                self.attendance_repo.register_attendance(student, sclass)

    def populate(self):
        aluno1 = Student("João", "123")
        self.user_repo.add_user(aluno1)

        aluno2 = Student("Maria", "123")
        self.user_repo.add_user(aluno2)

        aluno3 = Student("Eduardo", "123")
        self.user_repo.add_user(aluno3)

        aluno4 = Student("Eduarda", "123")
        self.user_repo.add_user(aluno4)

        aluno5 = Student("Isabel", "123")
        self.user_repo.add_user(aluno5)

        # Criando professor e suas turmas
        prof1 = Employee("Carlos", "123", "professor", "Matemática")
        self.user_repo.add_user(prof1)

        turma1 = SchoolClass(
            name="Matemática 1",
            teacher=prof1,
            schedule=datetime.time(9, 20),
            students=[aluno1, aluno2],
        )
        self.sclass_repo.create_sclass(turma1)
        turma2 = SchoolClass(
            name="Matemática 2",
            teacher=prof1,
            schedule=datetime.time(11, 10),
            students=[aluno3, aluno4],
        )
        self.sclass_repo.create_sclass(turma2)

        prova1_turma1 = Exam(turma1, "Prova 1 - Funções", datetime.date(2025, 8, 15))
        self.exam_repo.create_exam(turma1, prova1_turma1)

        self.exam_repo.register_grade(prova1_turma1, aluno1, 7.5)
        self.exam_repo.register_grade(prova1_turma1, aluno2, 10.0)
        prova1_turma1.grades_submitted = True

        prova2_turma1 = Exam(
            turma1, "Prova 2 - Análise Combinatória", datetime.date(2025, 9, 26)
        )
        self.exam_repo.create_exam(turma1, prova2_turma1)

        prova3_turma1 = Exam(
            turma1, "Prova 3 - Probabilidade", datetime.date(2025, 10, 29)
        )
        self.exam_repo.create_exam(turma1, prova3_turma1)

        prova1_turma2 = Exam(turma2, "Prova 1 - Vetores", datetime.date(2025, 10, 3))
        self.exam_repo.create_exam(turma1, prova1_turma2)

        prof2 = Employee("Luiz", "123", "professor", "Português")
        self.user_repo.add_user(prof2)

        turma3 = SchoolClass(
            name="Gramática 1",
            teacher=prof2,
            schedule=datetime.time(13, 30),
            students=[aluno1, aluno2],
        )
        self.sclass_repo.create_sclass(turma3)

        prof3 = Employee("Sergio", "123", "professor", "Educação Física")
        self.user_repo.add_user(prof3)

        eca1 = ECA(
            name="Natação",
            teacher=prof3,
            schedule=datetime.time(7, 30),
            students=[aluno2, aluno4],
        )
        self.eca_repo.create_eca(eca1)

        # Criando diretor
        diretor = Employee("Fernanda", "123", "diretor")
        self.user_repo.add_user(diretor)

        # Criando motorista
        motorista = Employee("José", "123", "motorista")
        self.user_repo.add_user(motorista)

        # Criando responsáveis
        responsavel = Guardian("Ana", "123", aluno2)
        self.user_repo.add_user(responsavel)

        responsavel2 = Guardian("Orlando", "123", aluno1)
        self.user_repo.add_user(responsavel2)

        responsavel3 = Guardian("Estefano", "123", aluno3)
        self.user_repo.add_user(responsavel3)

        responsavel4 = Guardian("Marlene", "123", aluno4)
        self.user_repo.add_user(responsavel4)

        responsavel5 = Guardian("Otavio", "123", aluno5)
        self.user_repo.add_user(responsavel5)
