# 📚 Sistema de Gestão Escolar

Projeto Original por **Zilderlan Naty dos Santos** ([link](https://github.com/Zilderlan09/School-Administration-System-OO)).

## 📋 Sobre o Projeto

Este sistema foi desenvolvido como projeto final da disciplina de **Projeto de Software** do curso de Sistemas de Informação da **Universidade Federal de Alagoas (UFAL)**, ministrada pelo professor Dr. **Baldoino Fonseca dos Santos Neto**.

O sistema simula um ambiente escolar com suporte para três tipos de usuários:

- 👨‍🎓 Alunos  
- 👨‍🏫 Funcionários (Professores, Diretores, Motoristas e Outros cargos)  
- 👪 Responsáveis (Pais ou responsáveis legais)

---

## 🛠️ Como Executar o Projeto

1. Instale o **Python 3.13 ou superior** ([Download aqui](https://www.python.org/downloads/))  
2. Clone ou baixe este repositório  
3. Coloque os arquivos `system.py` e `main.py` na mesma pasta  
4. No terminal, dentro da pasta do projeto, execute:

   ```bash
   python main.py

---

## Funcionalidades do sistema
- [x] **Student Enrollment**: Aluno pode ser cadastrado no sistema.
- [x] **Attendance Tracking**: O Professor pode registrar presenças para um Aluno. Essas informações ficam disponíveis para o próprio Aluno e para o Responsável.
- [x] **Parent Portal**: O Responsável tem a opção de ver um resumo das atividades do aluno, incluindo: Notas, próximas provas, presença e atividades extracurriculares.
- [x] **Class and Timetable Management**: O Usuário pode criar uma turma para um horário e adicionar alunos.
- [x] **Examination Management**: O usuário pode criar provas para uma turma.
- [x] **Gradebook Management**: O usuário pode cadastrar as notas das provas para cada aluno da turma.
- [x] **Extra-Curricular Activities Management**: O usuário pode criar uma atividade extracurricular e adicionar alunos.
- [x] **Course Material Distribution**: O Professor pode distribuir materiais de estudo para os alunos.
- [x] **Fee and Payment Processing**: O Responsável tem a opção de efetuar o pagamento da mensalidade por meio do PIX, Cartão ou Boleto. _O pagamento foi mockado devido à complexidade_.
- [x] **School Bus Tracking**: O Responsável tem a opção de rastrear o ônibus escolar do aluno. _O rastreamento foi mockado devido à complexidade_.

---

## Padrões de Projeto implementados
### Criacionais
Padrões implementados: **Singleton**, **Builder** e **Factory Method**

**Singleton**: A classe `School` concentra a gestão dos dados da instituição (possui as instâncias dos repositórios). Ao invés de passar a instância como argumento para várias partes do código, foi usado o padrão Singleton. Assim, basta instanciar a classe onde ela é necessária e teremos os mesmos dados. Tudo fica centralizado em uma única instância.

```python
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
         self.resource_adapter = ResourceToFileAdapter(
               service=CachedResourceProxy(upstream=MockResourceService())
         )

         self.populate()

         self._initialized = True

   def register_user(self, user: User):
      idx = self.user_repo.add_user(user)
      print(f"{user.get_type()} cadastrado (ID {idx})")
   
   # ...

# Uso:
class UserMenuStrategy(ABC):
   school: School
   menu_title: str
   logged_user: User

   def __init__(self):
      self.school = School() # Instanciada diretamente aqui. Acesso direto a todos os repositórios que possuem os dados
      self.set_menu_title()
      #  ....
```

**Builder**: A classe `SchoolClass` é um dos pontos chaves da aplicação. Como ela tem vários atributos, alguns opcionais para certas ocasições, o padrão builder é bem adequado. Também foi utilizado para construção do objeto `Employee` (`EmployeeBuilder`).

```python
class SchoolClassBuilder:
   def __init__(self):
      self._name: str | None = None
      self._teacher: Employee | None = None
      self._schedule: datetime.time | None = None
      self._students: list[Student] = []
      self._resources: list[Resource] = []
      self._n_classes_total: int = 0
      self._n_classes_passed: int = 0

   def set_name(self, name: str) -> "SchoolClassBuilder":
      self._name = name
      return self

   def set_teacher(self, teacher: Employee) -> "SchoolClassBuilder":
      self._teacher = teacher
      return self

   def set_schedule(self, schedule: datetime.time) -> "SchoolClassBuilder":
      self._schedule = schedule
      return self

   def add_student(self, student: Student) -> "SchoolClassBuilder":
      self._students.append(student)
      return self

   def add_resource(self, resource: Resource) -> "SchoolClassBuilder":
      self._resources.append(resource)
      return self

   def set_n_classes_total(self, total: int) -> "SchoolClassBuilder":
      self._n_classes_total = total
      return self

   def set_n_classes_passed(self, passed: int) -> "SchoolClassBuilder":
      self._n_classes_passed = passed
      return self

   def build(self) -> SchoolClass:
      if not self._name or not self._teacher or not self._schedule:
         raise ValueError("Turma requer nome, professor e horário")

      return SchoolClass(
         name=self._name,
         teacher=self._teacher,
         schedule=self._schedule,
         students=self._students,
         resources=self._resources,
         n_classes_total=self._n_classes_total,
         n_classes_passed=self._n_classes_passed,
      )

# Uso no cadastro de uma nova turma:
def input_school_class(teacher: Employee) -> SchoolClass:
    #...
    builder = SchoolClassBuilder()
    sclass = (
        builder.set_name(name)
        .set_teacher(teacher)
        .set_schedule(schedule)
        .set_n_classes_total(n_classes_total)
        .build()
    )
    # ...
```

**Factory Method**: Foi criada uma estrutura baseada em Factory Method para criação dos diferentes tipos de usuário, levando em consideração suas peculiaridades. A classe `Registrator` funciona como `Creator`.

```python
class Registrator(ABC):
   @abstractmethod
   def create_user(self) -> User:
      pass


class StudentRegistrator(Registrator):
   def create_user(self) -> User:
      print("--- Cadastro de Aluno ---")

      student_name = read_non_empty_string("Nome do aluno")
      student_password = read_non_empty_string("Senha do aluno")

      return Student(name=student_name, password=student_password)


class GuardianRegistrator(Registrator):
   def create_user(self) -> User:
      print("--- Cadastro de Responsável ---")
      guardian_name = read_non_empty_string("Nome do responsável")
      guardian_password = read_non_empty_string("Senha do responsável")

      school = School()
      student = select_item(
         school.get_alunos(),
         display_fn=lambda s: f"{s.name} (ID: {s.id})",
         title="Selecione um estudante",
      )

      if student is None:
         raise UserCreationError(
               "É necessário selecionar um aluno para cadastrar um responsável."
         )

      return Guardian(name=guardian_name, password=guardian_password, student=student)

# Uso no cadastro de usuários:
def register_users():
   # ...
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
   # ...
```

### Comportamentais
Padrões implementados: **Strategy**, **Template Method** e **Command**.

**Strategy**: Implementado para tratar de forma mais genérica e extensível os menus dos diferentes tipos de usuário da aplicação. O Strategy genérico é a classe `UserMenuStrategy` e o contexto `UserMenuContext`.

```python
class UserMenuStrategy(ABC):
   school: School
   menu_title: str
   logged_user: User

   def __init__(self):
      self.school = School()
      self.set_menu_title()

   def execute(self):
      self.set_logged_user()

      while True:
         os.system("clear")
         print(self.get_menu_title())

         self.show_menu_options()
         print("0. Voltar")

         selected_option = input("\nEscolha uma opção: ")
         os.system("clear")
         if selected_option == "0":
               break

         hold = self.match_option_to_function(selected_option)
         if hold:
               input("\nClique Enter para voltar ao menu.")

   def get_menu_title(self) -> str:
      return self.menu_title

   @abstractmethod
   def set_menu_title(self):
      pass

   @abstractmethod
   def set_logged_user(self):
      pass

   @abstractmethod
   def show_menu_options(self):
      pass

   @abstractmethod
   def match_option_to_function(self, selected_option: str) -> bool:
      pass

class UserMenuContext:
   strategy: UserMenuStrategy | None = None

   def show_menu(self):
      if self.strategy is None:
         raise ValueError("You must provide a strategy first")

      self.strategy.execute()

   def set_strategy(self, strategy: UserMenuStrategy):
      self.strategy = strategy
```

**Template Method**: A funcionalidade de menu é muito parecida em todas as suas versões. Template Method foi usado para criar um esqueleto geral deixando que a classe concreta substitua só duas partes: a listagem de opções do menu e o match da opção selecionada com o código correto da funcionalidade.

```python
# Por exemplo
class StudentMenuStrategy(UserMenuStrategy):
   student: Student

   def __init__(self, student: Student):
      self.student = student
      super().__init__()

   def set_menu_title(self):
      self.menu_title = f"🎓 Bem-vindo(a), {self.student.name}!"

   def set_logged_user(self):
      self.logged_user = self.student

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
```

**Command**: Implementado para abstrair a lógica de login e seleção do Strategy correto para cada usuário. Teve como resultado positivo a simplificação do método do menu de login.

```python
class LoginCommand(ABC):
   school: School
   user: User | None
   context: UserMenuContext

   def __init__(self, context: UserMenuContext):
      self.school = School()
      self.context = context

   def login(self):
      nome = input("\nNome: ")
      senha = input("Senha: ")

      self.user = self.school.login(nome, senha)

      print(f"\n✅ Login realizado como {self.user.get_type()}.")

   def execute(self):
      self.login()
      self.context.set_strategy(self.get_correct_strategy())

   @abstractmethod
   def get_correct_strategy(self) -> UserMenuStrategy:
      pass


class LoginAsStudentCommand(LoginCommand):
   def get_correct_strategy(self):
      if not self.user or not isinstance(self.user, Student):
         raise ValueError("User of wrong type")

      return LogMenuDectorator(StudentMenuStrategy(self.user))

# Outros para os outros tipos.
```

**Uso do padrão Command, que por sua vez, usa os demais**:
```python
# Na funcionalidade de login:

# ...
def show_login_menu(self):
   while True:
      os.system("clear")
      print("Selecione o tipo de usuário:")
      print("1 - Aluno")
      print("2 - Funcionário")
      print("3 - Responsável")
      print("0 - Voltar")
      option = input("\nEscolha uma opção: ")

      match option:
            case "1":
               command = LoginAsStudentCommand(self.context)
            case "2":
               command = LoginAsEmpoloyeeCommand(self.context)
            case "3":
               command = LoginAsGuardianCommand(self.context)
            case "0":
               break
            case _:
               input("❌ Opção inválida. Clique Enter para tentar novamente.")
               continue

      try:
            command.execute()
      except InvalidCredentialsException:
            input("❌ Credenciais inválidas. Clique Enter para tentar novamente.")
            continue

      self.context.show_menu()

      break
```

### Estruturais
Padrões implementados: **Decorator**, **Proxy** e **Adapter**.

**Decorator**: Implementado para adicionar registro de navegação dos usuários nos menus da aplicação. Assim, são registrar padrões de uso que podem ser estudadados para entender melhor os clientes. Os dados são salvos num arquivo `app.log`. Decorator é implementado com base no `UserMenuStrategy` pela classe `MenuDecorator` (classe abstrata) e `LogMenuDecorator` (implementação).

```python
class MenuDecorator(UserMenuStrategy):
   menu: UserMenuStrategy

   def __init__(self, menu: UserMenuStrategy) -> None:
      self.menu = menu

   def get_menu_title(self) -> str:
      return self.menu.get_menu_title()

   def set_menu_title(self):
      return self.menu.set_menu_title()

   def match_option_to_function(self, selected_option: str) -> bool:
      return self.menu.match_option_to_function(selected_option)

   def set_logged_user(self):
      self.menu.set_logged_user()

   def show_menu_options(self):
      self.menu.show_menu_options()


class LogMenuDectorator(MenuDecorator):
   def match_option_to_function(self, selected_option: str) -> bool:
      user_name = self.menu.logged_user.name
      menu_name = self.menu.__class__.__name__
      log = f"[{user_name}@{datetime.now()}] escolheu a opção {selected_option} no menu {menu_name}\n"

      with open(LOG_FILE_PATH, "a") as f:
         f.write(log)

      return self.menu.match_option_to_function(selected_option)

# Uso do decorator na criação dos menus:
class LoginAsGuardianCommand(LoginCommand):
   def get_correct_strategy(self):
      if not self.user or not isinstance(self.user, Guardian):
         raise ValueError("User of wrong type")

      return LogMenuDectorator(GuardianMenuStrategy(self.user))
```

**Proxy**: Foi utilizado como uma camada de Cache para um serviço externo de upload/download de recursos das aulas (_mock_), seguindo a mesma interface desse serviço. Essa classe verifica no cache interno a disponibilidade de arquivos para download, antes de fazer uma chamada para o serviço externo.

```Python
# Serviço externo (mock)
class ResourceService(ABC):
   @abstractmethod
   def upload(self, name: str, data: bytes) -> str:
      pass

   @abstractmethod
   def download(self, url: str) -> bytes:
      pass


class MockResourceService(ResourceService):
   def __init__(self):
      self._store: Dict[str, bytes] = {}

   def upload(self, name: str, data: bytes) -> str:
      key = hashlib.sha256((name + str(time.time())).encode()).hexdigest()
      url = f"https://mock.storage/{key}/{name}"
      self._store[url] = data

      print("⏳ Conectando ao serviço de armazenamento...")
      time.sleep(1)

      print("⬆️ Fazendo upload do recurso...")
      time.sleep(4)

      print("✅ Upload concluído.")

      return url

   def download(self, url: str) -> bytes:
      print("⏳ Conectando ao serviço de armazenamento...")
      time.sleep(1)

      if url not in self._store:
         raise FileNotFoundError(f"resource not found at {url}")

      print("⬇️ Fazendo download do recurso...")
      time.sleep(4)

      print("✅ Download concluído.")

      return self._store[url]

# Proxy (implementa mesma interface do serviço externo)
class CachedResourceProxy(ResourceService):
   def __init__(self, upstream: ResourceService):
      self._upstream = upstream
      self._store: Dict[str, bytes] = {}

   def upload(self, name: str, data: bytes) -> str:
      return self._upstream.upload(name, data)

   def is_cached(self, url: str) -> bool:
      return url in self._store

   def download(self, url: str) -> bytes:
      if self.is_cached(url):
         return self._store[url]

      data = self._upstream.download(url)
      self._store[url] = data

      return data

   def clear_cache(self):
      self._store.clear()
```

**Adapter**: Implementado para conectar o serviço de upload com a aplicação. O serviço de upload/download retorna bytes. Entretanto, a aplicação lida com o input de paths de arquivos para o upload e salvamento de arquivos numa pasta específica para download.

```python
class ResourceToFileAdapter:
   download_folder: Path

   def __init__(self, service: ResourceService, download_folder: str = "./resources"):
      self._service = service
      self.set_download_folder(download_folder)

   def set_download_folder(self, folder: str):
      self.download_folder = Path(folder).resolve()
      self.download_folder.mkdir(parents=True, exist_ok=True)

   def _filename_for_url(self, url: str) -> str:
      parsed = urlparse(url)
      name = Path(parsed.path).name

      if name:
         return name

      return hashlib.sha256(url.encode()).hexdigest()

   def upload_from_path(self, str_path: str) -> str:
      path = Path(str_path).resolve()

      if not path.exists():
         raise FileNotFoundError("O arquivo não existe.")

      if path.is_dir():
         raise ValueError("O path representa um diretório.")

      data = path.read_bytes()
      return self._service.upload(path.name, data)

   def download_to_folder(self, url: str) -> Path:
      data = self._service.download(url)

      filename = self._filename_for_url(url)
      path = self.download_folder / filename
      path.write_bytes(data)

      return path
```

**Uso do Proxy e adapter para acesso ao recurso externo**
```python
class School:
   # ...
   def __init__(self):
      if not self._initialized:
         # ...
         self.resource_adapter = ResourceToFileAdapter(
               service=CachedResourceProxy(upstream=MockResourceService())
         )
   # ...
```

## Gestão de exceções
A gestão de exceções foi aprimorada para garantir que o sistema se comporte como esperado, mesmo quando o usuário entra dados incorretos. As funções foram ajustadas para avisar ao usuário quando ele insere um dado inválido e permitir que ele tenta novamente. Abaixo são apresentados diferentes casos de tratamento de exceção no sistema.

**Entrada de campos de texto que não podem ser nulos**: Foi criada uma função auxiliar, pois esse caso aparecia muito. Quando o usuário entra uma string em branco, o código mostra um erro e pergunta novamente ao usuário.
```python
def read_non_empty_string(prop_name: str) -> str:
   while True:
      name = input(f"{prop_name}: ").strip()

      if len(name) == 0:
         print(f"{prop_name} não pode ser vazio.\n")
         continue

      return name

# Uso no cadastro de um aluno:
class StudentRegistrator(Registrator):
   def create_user(self) -> User:
      print("--- Cadastro de Aluno ---")

      student_name = read_non_empty_string("Nome do aluno")
      student_password = read_non_empty_string("Senha do aluno")

      return Student(name=student_name, password=student_password)
```

**Tratamento de erro na criação de usuário**: Usuário do responsável deve estar associado a um aluno. Foi criada uma exception customizada `UserCreationError`.
```python
class GuardianRegistrator(Registrator):
   def create_user(self) -> User:
      # ... 
      if student is None:
         raise UserCreationError(
               "É necessário selecionar um aluno para cadastrar um responsável."
         )
      # ...
```

**Entrada de datas e hora**: Também foram criadas funções auxiliares com o mesmo comportamento. Nesse caso, é tratado a exception `ValueError` que é lançada pela biblioteca `datetime` quando um valor inválido é inserido. Também foi adicionada uma checagem em que a data deve ser no futuro com exception customizada `InvalidExamDate`.

```python
def read_date() -> datetime.date:
   while True:
      date_str = input("Digite a data (YYYY-MM-DD): ")

      try:
         combined_str = f"{date_str}"
         scheduled_datetime = datetime.datetime.strptime(
               combined_str, "%Y-%m-%d"
         ).date()

         if scheduled_datetime < datetime.date.today():
               raise InvalidExamDate("Data deve ser no futuro.")

         return scheduled_datetime
      except ValueError:
         print("Formato de data inválido. Tente novamente.\n")
      except InvalidExamDate as e:
         print(f"{e}\n")


def read_time() -> datetime.time:
   while True:
      time_str = input("Horário da turma (HH:MM): ").strip()
      try:
         hour, minute = map(int, time_str.split(":"))
         return datetime.time(hour, minute)
      except ValueError:
         print("Formato inválido. Use HH:MM, por exemplo 14:30.\n")
```

**Seleção de múltiplas opções em uma lista**: Usado para selecionar múltiplos alunos. Os valores devem estar dentro das opções. A função é genérica e pode receber listas de qualquer tipo.
```python
def select_multiple_options(collection: list[T]) -> list[T]:
   while True:
      entrada = input("Digite os números separados por vírgula (ex: 1,3,5): ").strip()
      try:
         indices = [int(x) for x in entrada.split(",") if x.strip()]
         if not indices:
               raise ValueError
         if all(1 <= idx <= len(collection) for idx in indices):
               return [collection[idx - 1] for idx in indices]
         else:
               print("Algum número está fora da lista. Tente novamente.")
      except ValueError:
         print("Entrada inválida. Use números separados por vírgula.")
```

**Tratamento de saída do sistema por CTRL + C**
```python
#...
if __name__ == "__main__":
    try:
        app = App()
        app.start()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
```

**Tratamento de erro no login**: Foi criada uma exception customizada para tratar de credenciais incorretas, `InvalidCredentialsException`.
```python
def show_login_menu(self):
   # ...
   try:
         command.execute()
   except InvalidCredentialsException:
         input("❌ Credenciais inválidas. Clique Enter para tentar novamente.")
         continue

   self.context.show_menu()
```

**Tratamento de fornecimento de arquivos inválidos para o serviço de upload**: Trata tanto o arquivo não encontrado, quando o fornecimento de um dado inválido.
```python
try:
   str_path = read_non_empty_string("Path do material")
   url = self.school.resource_adapter.upload_from_path(
      str_path
   )
   break
except (FileNotFoundError, ValueError):
   print("Arquivo inválido. Tente novamente.")
   continue
```

**Tratamento do input de notas dos alunos**: Foi criada uma exception customizada `InvalidGradeException` que é lançada quando o usuário insere uma nota que não está entre 0 e 10. Também é tratada a entrada de valores não numéricos.
```python
resp = input(f"Nota de {student.name}? ").strip().lower()
try:
   grade = float(resp)
   if grade < 0 or grade > 10:
         raise InvalidGradeException(
            "A nota deve estar entre 0.0 e 10.0"
         )
   self.lancar_nota(exam, student, grade)
   break
except ValueError:
   print("    Entrada inválida.")
except InvalidGradeException as e:
   print(f"    {e}")
```

**Tratamento de escolha de opções de um menu**: Foi criada uma exception customizada para representar a seleção de uma opção inválida de um menu `InvalidMenuOptionException`. Usada na classe genérica de exibição de menu e input de opção. Nesse caso, também é tratada a inserção de um valor não numérico.
```python
def select_item(
    items: list[T],
    display_fn: Callable[[T], str] = str,
    title: str = "Selecione um item",
) -> T | None:
   # ...
   while True:
      try:
         escolha = int(input("\nDigite o número da opção: ").strip())
         if escolha == 0:
               return None
         elif 1 <= escolha <= len(items):
               return items[escolha - 1]
         else:
               raise InvalidMenuOptionException()
      except (ValueError, InvalidMenuOptionException):
         print("Entrada inválida. Digite um número dentro das opções.")
```