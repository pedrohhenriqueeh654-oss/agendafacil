# AgendaFácil 📅

**Sistema web de agendamento de serviços**

## Sobre o projeto

O AgendaFácil é um projeto acadêmico desenvolvido com o objetivo de facilitar a organização de horários e o agendamento de serviços oferecidos por profissionais autônomos e pequenos estabelecimentos.

A ideia surgiu da necessidade de tornar esse processo mais organizado. Muitos profissionais, como barbeiros, cabeleireiros e manicures, ainda administram seus atendimentos por mensagens, anotações ou agendas físicas. Embora esses métodos funcionem, podem dificultar a consulta dos horários disponíveis e aumentar o risco de reservas duplicadas.

O AgendaFácil busca oferecer uma alternativa prática, reunindo os serviços, os profissionais e os horários disponíveis em um único ambiente.

O projeto foi planejado como um **Produto Mínimo Viável (MVP)**, priorizando as funcionalidades necessárias para realizar um agendamento completo, sem adicionar recursos que aumentariam a complexidade da primeira versão.

## Objetivo

O principal objetivo do AgendaFácil é permitir que clientes encontrem horários disponíveis e realizem reservas de maneira organizada.

Para os profissionais, a proposta é facilitar o controle dos atendimentos e reduzir problemas relacionados à marcação manual de horários.

O sistema também foi pensado para pessoas com diferentes níveis de familiaridade com tecnologia. Por isso, a interface utiliza textos em português, campos identificados e uma navegação simples.

## Funcionalidades

A primeira versão do projeto contempla:

- Cadastro de usuários.
- Autenticação por e-mail e senha.
- Consulta de serviços disponíveis.
- Seleção do profissional responsável pelo atendimento.
- Consulta de datas e horários disponíveis.
- Realização de agendamentos.
- Verificação de conflitos entre reservas.
- Confirmação do agendamento com seus principais detalhes.
- Consulta das reservas realizadas.
- Interface web adaptável a computadores e celulares.

O foco é permitir que o usuário percorra o caminho desde a entrada no sistema até a confirmação de um horário.

## Tecnologias utilizadas

O AgendaFácil foi desenvolvido utilizando tecnologias que permitem organizar o código e implementar as funcionalidades sem depender de uma infraestrutura complexa.

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal do sistema |
| Django 5.2 LTS | Desenvolvimento da aplicação web |
| SQLite 3 | Armazenamento dos dados |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização e adaptação da interface |
| Git | Controle de versões |
| GitHub | Armazenamento e acompanhamento do código |

### Por que Python e Django?

A escolha do Python está relacionada à sua sintaxe organizada, à documentação disponível e à possibilidade de desenvolver diferentes funcionalidades com uma mesma linguagem.

O Django complementa essa escolha oferecendo recursos para autenticação, formulários, validação de dados e comunicação com o banco.

Esses recursos são importantes porque o projeto está sendo desenvolvido individualmente. Utilizar funcionalidades já disponíveis no framework permite dedicar mais atenção às regras de agendamento e aos testes.

### Banco de dados

O SQLite 3 foi escolhido por ser um banco de dados relacional que não exige a instalação de um servidor separado.

Ele permite armazenar as informações utilizadas pelo sistema, como usuários, profissionais, serviços, períodos disponíveis e agendamentos.

Para a fase inicial, com poucos usuários de teste, essa solução atende às necessidades do projeto.

Caso o AgendaFácil seja ampliado para atender um número maior de pessoas simultaneamente, poderá ser considerada uma migração para PostgreSQL.

## Organização do sistema

O projeto utiliza uma arquitetura monolítica em camadas.

Isso significa que suas funcionalidades fazem parte de uma mesma aplicação, mas o código é organizado de acordo com as responsabilidades de cada componente.

**Camada de apresentação:** contém as páginas, formulários, mensagens e demais elementos utilizados pelos usuários.

**Camada de lógica de negócio:** processa as solicitações, verifica os dados recebidos e aplica as regras necessárias para realizar os agendamentos.

**Camada de persistência:** realiza a comunicação com o banco de dados, permitindo cadastrar, consultar e atualizar informações.

Essa organização facilita a compreensão do projeto e permite realizar alterações em determinadas funcionalidades sem precisar modificar toda a aplicação.

## Como funciona um agendamento

O fluxo principal do AgendaFácil foi organizado para exigir poucas etapas do usuário.

1. O cliente acessa o sistema e entra em sua conta.
2. Consulta os serviços cadastrados.
3. Escolhe o serviço e o profissional desejado.
4. Seleciona uma data disponível.
5. Visualiza os horários oferecidos pelo sistema.
6. Escolhe o horário e confirma a solicitação.
7. Recebe uma confirmação com os detalhes da reserva.

Antes de registrar o agendamento, o sistema verifica se o horário continua disponível.

Essa validação é importante para evitar que dois clientes reservem o mesmo período para o mesmo profissional.

## Estrutura do projeto

A aplicação está organizada principalmente nos seguintes diretórios e arquivos:

```text
agendafacil/
├── agenda/
│   ├── management/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── booking.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── config/
├── manage.py
├── requirements.txt
└── README.md
```

O diretório `agenda` reúne as funcionalidades relacionadas aos serviços e agendamentos.

O arquivo `models.py` contém a definição dos dados utilizados pela aplicação. O `forms.py` organiza os formulários, enquanto o `views.py` trata as solicitações e respostas apresentadas aos usuários.

O arquivo `booking.py` concentra regras relacionadas à disponibilidade e à reserva de horários.

Já o diretório `config` contém as configurações principais do projeto Django.

## Como executar o projeto

Para executar o AgendaFácil localmente, é necessário ter o Python instalado no computador.

### 1. Obter os arquivos

Clone o repositório utilizando o Git ou baixe os arquivos diretamente pelo GitHub.

```bash
git clone https://github.com/pedrohenriqueeh654-oss/agendafacil.git
```

Entre na pasta que contém o arquivo `manage.py`.

### 2. Criar um ambiente virtual

No terminal, execute:

```bash
python -m venv .venv
```

No Windows, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o comando `python` não seja reconhecido, utilize o caminho do executável instalado no computador.

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Preparar o banco de dados

```bash
python manage.py migrate
```

Esse comando aplica as migrações necessárias para preparar a estrutura do banco de dados.

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

Após iniciar o servidor, acesse:

**http://127.0.0.1:8000/**

O endereço permite utilizar a aplicação localmente pelo navegador.

O servidor iniciado pelo comando `runserver` é destinado ao desenvolvimento e não deve ser utilizado diretamente em produção.

## Testes e validação

Os testes são uma parte importante do desenvolvimento do AgendaFácil, principalmente porque o sistema precisa manter a consistência dos horários reservados.

Entre os comportamentos que devem ser verificados estão:

- Cadastro e autenticação dos usuários.
- Exibição dos serviços disponíveis.
- Consulta de horários.
- Registro de reservas válidas.
- Impedimento de agendamentos conflitantes.
- Apresentação de mensagens de confirmação e erro.
- Funcionamento da navegação em telas menores.

O Django também permite executar testes automatizados por meio do comando:

```bash
python manage.py test
```

Esse comando executa os testes existentes no projeto. A cobertura deverá ser ampliada conforme novas funcionalidades forem implementadas.

Além dos testes técnicos, o planejamento acadêmico prevê uma avaliação da interface com um representante do público-alvo, utilizando tarefas relacionadas ao fluxo de agendamento.

## Acessibilidade

Uma das preocupações do projeto é permitir que pessoas com conhecimentos básicos de informática consigam utilizar o sistema.

Por esse motivo, o planejamento da interface considera:

- Textos e instruções em linguagem simples.
- Identificação dos campos dos formulários.
- Contraste adequado entre textos e fundos.
- Botões com tamanho apropriado para interação.
- Mensagens que não dependam exclusivamente de cores.
- Navegação consistente entre as páginas.
- Adaptação para dispositivos móveis.

Esses aspectos deverão ser avaliados durante os testes de usabilidade para identificar dificuldades e oportunidades de melhoria.

## Segurança e privacidade

O AgendaFácil utiliza os mecanismos de autenticação e proteção disponibilizados pelo Django.

O projeto prevê validação dos dados no servidor, controle de acesso às operações protegidas e armazenamento seguro das senhas por meio dos mecanismos de hash do framework.

Também é importante manter informações de configuração e credenciais fora do repositório público.

O banco de dados utilizado durante o desenvolvimento deve conter apenas informações fictícias de demonstração.

A aplicação ainda deverá passar por verificações adicionais antes de qualquer utilização com dados reais ou disponibilização pública.

## Limitações da primeira versão

Como o AgendaFácil é um MVP acadêmico, algumas funcionalidades mais avançadas não fazem parte do escopo inicial.

Entre as possibilidades de evolução estão notificações automáticas, integração com calendários externos, relatórios de atendimento e recursos administrativos adicionais.

A prioridade atual é garantir que as funcionalidades essenciais estejam organizadas, compreensíveis e funcionando corretamente.

## Possibilidades de evolução

Depois da validação da primeira versão, o projeto poderá receber melhorias baseadas nas dificuldades identificadas durante os testes.

Algumas possibilidades são:

- Envio de lembretes de agendamento.
- Painel de gerenciamento para profissionais.
- Relatórios de horários e atendimentos.
- Configuração de dias e períodos especiais.
- Melhorias na experiência de uso pelo celular.
- Implantação em um servidor acessível pela internet.
- Migração para um banco de dados mais adequado a múltiplos acessos simultâneos.

Essas melhorias serão avaliadas conforme a necessidade, evitando adicionar complexidade antes de validar o funcionamento principal.

## Contexto acadêmico

O AgendaFácil foi desenvolvido como parte de uma experiência prática de desenvolvimento de software.

O trabalho envolve identificação de um problema, definição do público-alvo, pesquisa de soluções semelhantes, planejamento da arquitetura, escolha das tecnologias, modelagem dos dados, implementação do MVP e preparação de testes de validação.

A proposta é aplicar os conhecimentos adquiridos durante os estudos na construção de uma solução relacionada a uma necessidade presente no cotidiano de pequenos prestadores de serviços.

## Considerações finais

Desenvolver o AgendaFácil tem sido uma oportunidade de compreender melhor como diferentes partes de um sistema se relacionam.

O projeto não envolve apenas criar telas ou escrever código. Também exige pensar nas necessidades dos usuários, definir regras de funcionamento, organizar os dados e identificar possíveis problemas antes que eles prejudiquem a experiência de uso.

A escolha de Python, Django e SQLite permitiu construir uma base para o sistema sem depender de ferramentas excessivamente complexas.

O próximo objetivo é continuar aprimorando a aplicação, realizando testes e corrigindo os problemas encontrados, sempre mantendo o foco na proposta inicial: facilitar o agendamento de serviços de maneira organizada e acessível.

---

**AgendaFácil — Projeto acadêmico de desenvolvimento de software.**

## Revisão técnica do projeto

Esta etapa tem como objetivo revisar a organização e a qualidade do código do AgendaFácil antes de integrar novas alterações à versão principal.

A revisão será concentrada em quatro aspectos: separação das responsabilidades entre os arquivos, clareza das regras de agendamento, validação das informações recebidas e proteção dos dados dos usuários.

Também serão observados possíveis pontos de melhoria na manutenção do sistema, considerando que o projeto utiliza Python, Django e SQLite.

As observações identificadas durante a análise serão registradas no Pull Request, permitindo acompanhar o que foi verificado e quais ajustes poderão ser necessários futuramente.
