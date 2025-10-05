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
- **Singleton**: A classe `School` concentra a gestão dos dados da instituição (possui as instâncias dos repositórios). Ao invés de passar a instância como argumento para várias partes do código, foi usado o padrão Singleton. Assim, basta instanciar a classe onde ela é necessária e teremos os mesmos dados. Tudo fica centralizado em uma única instância.
- **Builder**: A classe `SchoolClass` é um dos pontos chaves da aplicação. Como ela tem vários atributos, alguns opcionais para certas ocasições, o padrão builder é bem adequado.
- **Factory Method**: Foi criada uma estrutura baseada em Factory Method para criação dos diferentes tipos de usuário, levando em consideração suas peculiaridades. A classe `Registrator` funciona como `Creator`.

### Comportamentais
- **Strategy**: Implementado para tratar de forma mais genérica de extensível os menus dos diferentes tipos de usuário da aplicação.
- **Template Method**: A funcionalidade de menu é muito parecida em todas as suas versões. Template Method foi usado para criar um esqueleto geral deixando que a classe concreta substitua só duas partes: a listagem de opções do menu e o match da opção selecionada com o código correto da funcionalidade.