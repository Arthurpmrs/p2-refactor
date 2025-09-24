# 📚 Sistema de Gestão Escolar

Projeto Original por **Zilderlan Naty dos Santos** ([link](https://github.com/Zilderlan09/School-Administration-System-OO)).

## 📋 Sobre o Projeto

Este sistema foi desenvolvido como projeto final da disciplina de **Projeto de Software** do curso de Sistemas de Informação da **Universidade Federal de Alagoas (UFAL)**, ministrada pelo professor Dr. **Baldoino Fonseca dos Santos Neto**.

O sistema simula um ambiente escolar com suporte para três tipos de usuários:

- 👨‍🎓 Alunos  
- 👨‍🏫 Funcionários (Professores, Diretores, Motoristas e Outros cargos)  
- 👪 Responsáveis (Pais ou responsáveis legais)

---
## Funcionalidades do sistema
- **Student Enrollment**: Aluno pode ser cadastrado no sistema.
- **Attendance Tracking**: O Professor pode registrar presenças para um Aluno. Essas informações ficam disponíveis para o próprio Aluno e para o Responsável.
- **Parent Portal**: O Responsável tem a opção de ver um resumo das atividades do aluno, incluindo: Notas, próximas provas, presença e atividades extracurriculares.
- **Class and Timetable Management**: O Usuário pode criar uma turma e adicionar alunos.
- **Examination Management**: O usuário pode criar provas para uma turma.
- **Gradebook Management**: O usuário pode cadastrar as notas das provas para cada aluno da turma.
- **Extra-Curricular Activities Management**: O usuário pode criar uma atividade extracurricular e adicionar alunos.
- **Course Material Distribution**: O Professor pode distribuir materiais de estudo para os alunos
- **Fee and Payment Processing**: O Responsável tem a opção de efetuar o pagamento da mensalidade por meio do PIX, Cartão ou Boleto. _O pagamento foi mockado devido à complexidade_.
- **School Bus Tracking**: O Responsável tem a opção de rastrear o ônibus escolar do aluno. _O rastreamento foi mockado devido à complexidade_.

---

## 🛠️ Como Executar o Projeto

1. Instale o **Python 3.6 ou superior** ([Download aqui](https://www.python.org/downloads/))  
2. Clone ou baixe este repositório  
3. Coloque os arquivos `system.py` e `main.py` na mesma pasta  
4. No terminal, dentro da pasta do projeto, execute:

   ```bash
   python main.py
