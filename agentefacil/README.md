# AgendaFácil

MVP acadêmico de agendamento de serviços para profissionais autônomos e pequenos estabelecimentos. Aplicação web responsiva em português, com Python, Django 5.2 LTS, SQLite 3 e páginas HTML/CSS.

## Executar no VS Code (Windows)

Pré-requisito: Python 3.12 com o comando `py` disponível. Abra no VS Code a pasta que contém o arquivo `manage.py`, depois abra **Terminal → Novo Terminal**. Execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py dados_demo
.\.venv\Scripts\python.exe manage.py runserver
```

Abra **http://127.0.0.1:8000/** no navegador. Não é necessário ativar o ambiente nem alterar a política de execução do PowerShell. Em Linux e macOS, use `python3 -m venv .venv` e troque o caminho do executável por `./.venv/bin/python`. Encerre o servidor com **Ctrl+C**.

## Demonstrar

1. Crie uma conta com perfil **Cliente** e um e-mail fictício, como `ana@agenda.example`. Escolha uma senha de teste que você não usa em outra conta.
2. Em **Agendar**, selecione **Corte masculino — Carlos Lima**. Escolha uma data futura de **segunda a sábado** e clique em **Consultar horários**.
3. Selecione um horário, confirme e confira os dados da reserva. Em **Minhas reservas**, é possível voltar aos detalhes.
4. Para demonstrar o painel do profissional, crie outra conta com perfil **Profissional**. Cadastre um serviço e um período semanal de atendimento. A conta fictícia do Carlos não permite login.

## Arquitetura e escopo

- **Apresentação** — templates Django e CSS em `agenda/templates/` e `agenda/static/`.
- **Lógica de negócio** — `agenda/booking.py` calcula horários e recusa conflitos. A disponibilidade é conferida novamente no momento da gravação. No SQLite, a transação IMMEDIATE impede duas gravações concorrentes de validar o mesmo período livre.
- **Persistência** — ORM e migrações do Django. As entidades são Usuários, Serviços, Disponibilidades e Agendamentos.
- **Requisitos do MVP** — cadastro e autenticação, cadastro de serviços, configuração de disponibilidade, consulta de horários, reserva e confirmação. Cada cliente vê apenas suas reservas. Cada profissional administra seus próprios serviços e períodos.
- **Fora desta versão** — cancelamento pelo cliente, pagamentos, lembretes, avaliações e recuperação de senha por e-mail. O servidor de desenvolvimento é somente para uso local. Implantação online, métricas com representante externo e auditoria completa de acessibilidade não fazem parte desta entrega. Para implantação real, configure HTTPS, armazenamento persistente, backups, proteção contra tentativas repetidas de login e variáveis de ambiente `AGENDA_DEBUG=0`, `AGENDA_SECRET_KEY` e `AGENDA_ALLOWED_HOSTS`. O servidor incluído não é para produção.

## Testes automatizados

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Os testes cobrem cadastro e login, proteção de dados entre contas, CSRF, cadastro de serviços e disponibilidade, confirmação, recusa de conflito e duas solicitações simultâneas para períodos sobrepostos.

## Publicar no GitHub

Crie na sua conta um repositório público e vazio chamado `agendafacil`. Não inicialize com README, licença ou gitignore, pois os arquivos do projeto já estão na pasta. No terminal do VS Code, substitua `SEU-USUARIO` pelo seu usuário real e execute:

```text
git init -b main
git add .
git status --short
git commit -m "Adiciona MVP do AgendaFacil"
git remote add origin https://github.com/SEU-USUARIO/agendafacil.git
git push -u origin main
```

Antes do commit, confirme que `.venv`, `db.sqlite3`, `test.sqlite3` e `.env` não aparecem na lista. Se o Git pedir autenticação, conclua pelo GitHub no navegador. Abra a URL pública em uma janela anônima e use esse endereço no formulário da faculdade. Se for solicitada uma evidência, capture a página do repositório com a lista de arquivos e o README.
