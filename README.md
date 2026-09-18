<div align="center">

<img src="https://github.com/jcarlossc/etl-python-gmail-mysql/blob/main/images/etk_python_gmail_mysql.jpg">

# ETL Python Gmail → MySQL

Pipeline ETL desenvolvido em Python para **extração de arquivos enviados por e-mail via Gmail**, validação, padronização, limpeza, 
integração de dados de vendas e clientes e armazenamento em um **banco de dados MySQL estruturado em Star Schema**.

O projeto foi desenvolvido com foco em **automação, qualidade dos dados, modularidade, testabilidade e organização de um pipeline de 
dados próximo a um cenário real de produção**.

[![CI](https://github.com/jcarlossc/etl-python-gmail-mysql/actions/workflows/ci.yml/badge.svg)](https://github.com/jcarlossc/etl-python-gmail-mysql/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-60A5FA.svg)](https://python-poetry.org/)
[![MySQL](https://img.shields.io/badge/MySQL-database-4479A1.svg)](https://www.mysql.com/)
[![Pandas](https://img.shields.io/badge/Pandas-data%20processing-150458.svg)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-testing-0A9EDC.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

## 📌 Imagens do Projeto
<table>
  <tr>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-gmail-mysql/blob/main/images/2a8d705c-a1ae-456c-86e8-133101834270.jpg" alt="Imagem Fluxo" width="250" target="_blank"/>
        <figcaption>
          <p><b>Diagrama</b></p>
        </figcaption>
      <figure>
    </td>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-gmail-mysql/blob/main/images/cobertura.jpg" alt="Imagem Testes" width="250" target="_blank"/>
        <figcaption>
          <p><b>Cobertura de Testes</b></p>
        </figcaption>
      <figure>
  </td>
  <td>
    <figure>
      <img src="https://github.com/jcarlossc/etl-python-gmail-mysql/blob/main/images/pytest.PNG" alt="Imagem Testes" width="250" target="_blank" />
      <figcaption>
          <p><b>Pytest</b></p>
      </figcaption>
    <figure>
  </td>
   <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-gmail-mysql/blob/main/images/etk_python_gmail_mysql.jpg" alt="Imagem Fluxo" width="250" target="_blank"/>
        <figcaption>
          <p><b>Cobertura de Testes</b></p>
        </figcaption>
      <figure>
  </td>
  </tr>
</table>

## 📌 Visão geral

O `etl_python_gmail_mysql` automatiza o processo de transformação de arquivos recebidos por e-mail em dados estruturados e prontos para análise.

O fluxo contempla:

```text
Gmail
   ↓
Extração de anexos
   ↓
Staging
   ↓
Validação dos arquivos
   ↓
Padronização dos dados
   ↓
Limpeza e sanitização
   ↓
Integração de vendas + clientes
   ↓
Star Schema
   ↓
MySQL
   ↓
BI / Analytics
```
A aplicação também possui mecanismos de:

* configuração externa;
* logging;
* retry;
* validação de arquivos;
* validação de tipos;
* tratamento de CSV e XLSX;
* sanitização de dados;
* integração entre datasets;
* criação do banco de dados;
* criação do modelo dimensional;
* testes automatizados;
* análise de cobertura;
* integração contínua.

## 🏗️ Arquitetura do Pipeline

Fluxo de processamento

### 1. Extração do Gmail

O pipeline utiliza a API do Gmail para:

* autenticar a aplicação;
* acessar mensagens de uma determinada label;
* localizar mensagens disponíveis para processamento;
* identificar anexos;
* realizar o download dos arquivos.

Principais componentes:
```
services/
└── gmail/
    ├── authentication.py
    ├── labels.py
    ├── messages.py
    └── attachments.py
```

### 2. Staging

Os arquivos extraídos do Gmail são armazenados em uma camada intermediária de staging.

Essa etapa permite separar os dados recebidos da etapa de processamento.

Exemplo:
```
data/
├── downloads/
├── stagings/
│   ├── csv/
│   └── xlsx/
└── processed/
```

O staging funciona como uma área de preparação antes da validação e transformação dos dados.

### 3. Validação dos arquivos

Antes de processar os dados, o pipeline realiza validações relacionadas aos arquivos recebidos.

São verificadas condições como:

* existência do arquivo;
* extensão permitida;
* arquivo vazio;
* estrutura do CSV;
* estrutura do XLSX;
* colunas esperadas;
* consistência dos dados.

Estrutura:
```
validation/
├── validate_file_exists.py
├── validate_file_extension.py
├── validate_file_not_empty.py
├── validation_csv.py
└── validation_xlsx.py
```

Essa camada impede que arquivos inválidos avancem para as etapas seguintes do pipeline.

### 4. Padronização dos dados

Após a validação, os dados são carregados em DataFrames e têm seus tipos e estruturas padronizados.
```
standardization/
└── validate_types.py
```

Essa etapa é importante para garantir consistência antes da integração dos datasets.

### 5. Limpeza e sanitização

Os dados passam por processos de limpeza e sanitização.

Exemplos:

* tratamento de nomes;
* padronização de valores;
* sanitização de campos;
* normalização de informações;
* preparação dos dados para integração.

Estrutura:
```
cleanning/
└── clean_data.py

utils/
├── clean/
│   └── clean_name.py
└── sanitize/
    └── get_sanitize.py
```

Observação: o diretório cleanning mantém atualmente a nomenclatura utilizada no projeto. Em uma futura refatoração, pode ser renomeado para cleaning.

### 6. Integração de vendas e clientes

Após o tratamento individual dos datasets, os dados de vendas e clientes são integrados.
```
integration/
└── integrate_sales_clients.py
```

A integração permite relacionar informações como:
```
Clientes
   │
   │ id_cliente
   ↓
Vendas
```

Essa etapa prepara os dados para a construção do modelo dimensional.

## ⭐ Modelagem dimensional

O projeto utiliza uma arquitetura baseada em Star Schema.
```
                 dim_cliente
                     │
                     │
dim_tempo ───── fato_vendas ───── dim_produto
                     │
                     │
                outras dimensões

```

O objetivo é organizar os dados de forma adequada para:

* consultas analíticas;
* criação de dashboards;
* geração de KPIs;
* relatórios;
* ferramentas de Business Intelligence.

A criação do modelo está centralizada em:
```
schema/
└── create_star_schema.py
```

## 🗄️ Banco de dados MySQL

O pipeline cria e utiliza um banco de dados MySQL para armazenamento dos dados processados.

Componentes:
```
database/
└── connection_db.py

sql/
├── create_sales_database.sql
└── execute_sql.py
```

A camada de banco é responsável por:

* estabelecer conexão;
* executar scripts SQL;
* criar estruturas necessárias;
* persistir os dados;
* encerrar conexões de forma segura.

A conexão é realizada utilizando SQLAlchemy.

## 🔄 Orquestração do pipeline

A execução das etapas é centralizada no módulo:
```
pipeline/
└── run_pipeline.py
```
O ponto de entrada da aplicação é:

main.py

Conceitualmente:
```
main.py
   │
   ↓
run_pipeline()
   │
   ├── Configuração
   ├── Logging
   ├── Gmail
   ├── Download
   ├── Staging
   ├── Validação
   ├── Padronização
   ├── Limpeza
   ├── Integração
   ├── Star Schema
   ├── MySQL
   └── Finalização
```
Isso mantém a execução do pipeline centralizada e facilita sua manutenção.

## ⚙️ Configuração

As configurações da aplicação são separadas do código.

Principais recursos:
```
.env
.env.example
```
e:
```
utils/
├── settings/
│   └── Settings.py
└── yaml/
    └── get_yaml.py
```
A utilização de arquivos de configuração permite alterar parâmetros do ambiente sem modificar diretamente a implementação.

Exemplo:

* DB_HOST=localhost
* DB_PORT=3306
* DB_USER=usuario
* DB_PASSWORD=senha
* DB_NAME=banco

Nunca versione credenciais reais, tokens OAuth ou informações sensíveis.

## 🔐 Autenticação Gmail

A integração com o Gmail utiliza autenticação OAuth.

Arquivos relacionados:

* credentials.json
* token.json

Esses arquivos são específicos do ambiente e não devem ser publicados no GitHub.

O repositório deve utilizar:
```
.env.example
```
como referência para as variáveis necessárias.

## 📝 Logging

O projeto possui uma camada dedicada de logging:
```
utils/
└── loggers/
    └── logger.py
```
Os eventos da aplicação são registrados em:
```
logs/
└── app.log
```
O logging permite acompanhar:

* início do pipeline;
* execução das etapas;
* erros;
* exceções;
* processamento dos arquivos;
* operações no banco;
* conclusão do pipeline.

Exemplo conceitual:
```
2026-09-18 11:40:53,251 - INFO - etl_python_gmail_mysql.utils.loggers.logger - Logger configurado com sucesso.
2026-09-18 11:41:25,722 - INFO - etl_python_gmail_mysql.pipeline.run_pipeline - Iniciando pipeline ETL.
2026-09-18 11:41:25,816 - INFO - etl_python_gmail_mysql.pipeline.run_pipeline - Settings carregadas.
2026-09-18 11:41:25,816 - INFO - etl_python_gmail_mysql.services.gmail.authentication - Iniciando autenticação no Gmail
2026-09-18 11:41:25,831 - INFO - etl_python_gmail_mysql.services.gmail.authentication - Gmail autenticado com sucesso
2026-09-18 11:41:25,941 - INFO - googleapiclient.discovery_cache - file_cache is only supported with oauth2client<4.0.0
2026-09-18 11:41:26,034 - INFO - etl_python_gmail_mysql.pipeline.run_pipeline - Autenticação Gmail concluída.
2026-09-18 11:41:26,034 - INFO - etl_python_gmail_mysql.services.gmail.labels - Iniciando aquisição de ID de labels
2026-09-18 11:41:29,552 - INFO - etl_python_gmail_mysql.services.gmail.labels - Labels adiquiridas con sucesso: EMPRESA/01_ENTRADA
2026-09-18 11:41:29,552 - INFO - etl_python_gmail_mysql.services.gmail.messages - Iniciando aquisição de mensagens de labels
2026-09-18 11:41:29,896 - INFO - etl_python_gmail_mysql.services.gmail.messages - Mensagens adiquiridas com sucesso
2026-09-18 11:41:29,896 - INFO - etl_python_gmail_mysql.pipeline.run_pipeline - Mensagens encontradas: 4
2026-09-18 11:41:29,896 - INFO - etl_python_gmail_mysql.services.gmail.attachments - Iniciando download de anexos
2026-09-18 11:41:30,599 - INFO - etl_python_gmail_mysql.services.gmail.attachments - Anexo salvo com sucesso: 2026_08_26_17_04_57_vendas_janeiro.csv
2026-09-18 11:41:30,599 - INFO - etl_python_gmail_mysql.services.gmail.attachments - Término dos downloads dos anexos
...
```

## 🔁 Retry

Operações sujeitas a falhas temporárias possuem suporte a retry:
```
services/
└── retry.py
```
O objetivo é aumentar a resiliência do pipeline em operações como:

comunicação com APIs;
conexão com serviços externos;
comunicação com MySQL;
operações sujeitas a falhas transitórias.

## 🧪 Testes

O projeto possui testes automatizados utilizando pytest.

Estrutura:
```
tests/
├── test_attachments.py
├── test_authentication.py
├── test_clean_data.py
├── test_clean_names.py
├── test_connection_db.py
├── test_create_star_schema.py
├── test_execute_sql.py
├── test_files_exists.py
├── test_get_sanitize.py
├── test_get_staging.py
├── test_get_yaml.py
├── test_integrate_sales_clients.py
├── test_labels.py
├── test_logger.py
├── test_main.py
├── test_messages.py
├── test_retry.py
├── test_run_pipeline.py
├── test_settings.py
├── test_validate_csv.py
├── test_validate_file_exists.py
├── test_validate_file_extension.py
├── test_validate_file_not_empty.py
├── test_validate_types.py
└── test_validation_xlsx.py
```

## 📁 Estrutura do projeto
```
etl_python_gmail_mysql/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│    ├── columns_types.yaml
│    ├── gmail.yaml
│    └── logging.yaml
├── data/
│    ├── downloads/
│    └── stagings/
│          ├── csv/
│          └── xlsx
├── htmlcov/
├── images/
├── logs/
│   └── app.log
├── src/
│   └── etl_python_gmail_mysql/
│       ├── main.py
│       ├── __init__.py
│       ├── cleanning/
│       │   └── clean_data.py
│       ├── database/
│       │   └── connection_db.py
│       ├── integration/
│       │   └── integrate_sales_clients.py
│       ├── pipeline/
│       │   └── run_pipeline.py
│       ├── schema/
│       │   └── create_star_schema.py
│       ├── services/
│       │   ├── retry.py
│       │   └── gmail/
│       │       ├── authentication.py
│       │       ├── labels.py
│       │       ├── messages.py
│       │       └── attachments.py
│       ├── sql/
│       │   ├── create_sales_database.sql
│       │   └── execute_sql.py
│       ├── staging/
│       │   └── get_staging.py
│       ├── standardization/
│       │   └── validate_types.py
│       ├── utils/
│       │   ├── clean/
│       │   │     └── clean_name.py
│       │   ├── files_exists/
│       │   │     └── get_file.py
│       │   ├── loggers/
│       │   │     └── logger.py
│       │   ├── sanitize/
│       │   │     └── get_sanitize.py
│       │   ├── settings/
│       │   │     └── Settings.py
│       │   └── yaml/
│       │         └── get_yaml.py
│       └── validation/
│           ├── validate_file_exists.py
│           ├── validate_file_extension.py
│           ├── validate_file_not_empty.py
│           ├── validation_csv.py
│           └── validation_xlsx.py
├── tests/
│   ├── test_attachments.py
│   ├── test_authentication.py
│   ├── test_clean_data.py
│   ├── test_clean_names.py
│   ├── test_connection_db.py
│   ├── test_create_star_schema.py
│   ├── test_execute_sql.py
│   ├── test_files_exists.py
│   ├── test_get_sanitize.py
│   ├── test_get_staging.py
│   ├── test_get_yaml.py
│   ├── test_integrate_sales_clients.py
│   ├── test_labels.py
│   ├── test_logger.py
│   ├── test_main.py
│   ├── test_messages.py
│   ├── test_retry.py
│   ├── test_run_pipeline.py
│   ├── test_settings.py
│   ├── test_validate_csv.py
│   ├── test_validate_file_exists.py
│   ├── test_validate_file_extension.py
│   ├── test_validate_file_not_empty.py
│   ├── test_validate_types.py
│   └── test_validation_xlsx.py
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
```

## ⚙️ Tecnologias
| Tecnologia | Utilização |
| ---------- | ---------- |
| Python | Desenvolvimento do ETL |
| Poetry | Gerenciamento de dependências |
| Gmail API | Extração dos e-mails e anexo |
| Pandas | Manipulação e transformação |
| SQLAlchemy | Conexão com banco de dados |
| MySQL | Armazenamento |
| Pydantic | Settings	Configurações da aplicação |
| PyYAML | Configurações YAML |
| Pytest | Testes automatizados |
| Pytest-Cov | Cobertura de testes |
| Ruff | Linting e formatação |
| MyPy | Verificação estática |
| Pre-commit | Automação de validações |
| GitHub Actions | CI/CD |
| Release Please | Automatização de releases |
| XAMPP | Servidor web local |

## 🔎 Qualidade de código
As validações são utilizadas para manter consistência, tipagem e qualidade do código.

* App: Executa aplicação. ```poetry run task app```
* Ruff:
    * format: altera os arquivos para deixá-los formatados. ```poetry run task format```
    * check: apenas verifica se os arquivos estão formatados. Não altera nada. ```poetry run task check```
    * lint: procura problemas como imports incorretos, código desnecessário, variáveis não utilizadas, etc. ```poetry run task lint```
    * fix: procura esses problemas e tenta corrigi-los automaticamente. ```poetry run task fix```
* Pytest: executa testes unitários. ```poetry run task pytest```
* Covhtml: executa os testes e gera relatório de cobertura em HTML. ```poetry run task covhtml```. (htmlcov//index.html) 
* Covcmd: Executa testes mostrando cobertura no terminal. ```poetry run task covcmd```
* Mypy: Faz verificação estática de tipos. ```poetry run task mypy```
* Precommit</span>: Executa todos os hooks do pre-commit. ```poetry run task precommit```

## 🔬 Qualidade e engenharia

O projeto foi estruturado seguindo princípios de engenharia de software aplicados a pipelines de dados:

* separação de responsabilidades;
* arquitetura modular;
* configuração externa;
* tratamento de exceções;
* logging;
* retry;
* validação de dados;
* tipagem estática;
* testes automatizados;
* cobertura de testes;
* linting;
* formatação automática;
* integração contínua;
* versionamento;
* automação de releases.

## 🔐 Segurança

Informações sensíveis não devem ser armazenadas no código-fonte.

Arquivos como:

.env
credentials.json
token.json

devem permanecer protegidos e adicionados ao .gitignore.

O repositório fornece:
```
.env.example
```
para documentar as configurações necessárias sem expor credenciais.

## 🛠️ Modo de Utilização
1. GMAIL API:
* Logado com Gmail, Acesse: ```https://cloud.google.com/```
* Clique no menu suspenso de projetos no topo da página e selecione Novo Projeto.
* Digite um nome para o seu projeto e clique em Criar.
* No menu lateral esquerdo, vá em APIs e Serviços e depois em Biblioteca.
* Na barra de pesquisa, digite Gmail API.
* Clique na API do Gmail e depois no botão Ativar.
* Vá em APIs e Serviços > Tela de permissão OAuth.
* Selecione o tipo de usuário como Interno ou Externo (use Externo se for para testes pessoais com contas livres) e clique em Criar.
* Preencha o nome do aplicativo e o seu e-mail de suporte.
* Avance pelas telas, adicione seu e-mail de contato e finalize a configuração.
* No menu lateral, acesse Clientes dentro da seção de autenticação (ou Credenciais > Criar credenciais > ID do cliente OAuth).
* Escolha o tipo de aplicativo como App para computador (Desktop app).
* Dê um nome para a credencial e clique em Criar.
* Faça o download do arquivo JSON gerado.
* Renomeie esse arquivo para credentials.json e coloque-o na raiz do projeto, e o mais IMPORTANTE: não versioná-lo, ou seja, colocá-lo no ```.gitignore```
* Adicione um usuário de teste.
* Obs: no primeiro acesso o Gmail pedirá confirmação de usuário pelo navegador e, após confirmação, um arquivo chamado ```token.json``` será criado na raiz do sistema e que também não deverá ser versionado.

2. Execute o XAMPP
* Caso não o tenha, baixe-o: <a href="https://www.apachefriends.org/pt_br/download.html">https://www.apachefriends.org/pt_br/download.html</a>
* Instale-o normalmente
* Execute o Painel de Controle
* Acione o Apache e o MySQL/MariaDB

3. Com a linguagem Python instalada: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>
* Instale o pipx:
```
pip install pipx
```
* Em seguida:
```
pipx ensurepath
```
* E, por fim, o gerenciador Poetry:
```
pipx install poetry
```
4. Clone o repositório e acesse o diretório
```
git clone https://github.com/jcarlossc/etl-python-gmail-mysql.git
cd etl-python-gmail-mysql
```
* Instalação das dependências:
```
poetry install
```
* Para executar o projeto:
```
poetry run task app
```

## 📈 Possibilidades de utilização

O pipeline pode servir como base para cenários em que arquivos são recebidos periodicamente por e-mail e precisam ser incorporados automaticamente a uma plataforma de dados.

Exemplos:
```
E-commerce
     ↓
Relatórios de vendas
     ↓
Gmail
     ↓
ETL
     ↓
MySQL
     ↓
Power BI / Tableau / Qlik
```
O mesmo padrão pode ser adaptado para diferentes fontes e formatos de dados.

## 🎯 Objetivos do projeto

Este projeto demonstra conhecimentos práticos em:

Engenharia de Dados;
construção de pipelines ETL;
integração com APIs;
processamento de arquivos;
tratamento e validação de dados;
Python para dados;
modelagem dimensional;
bancos relacionais;
SQL;
automação;
testes;
qualidade de código;
CI/CD;
boas práticas de desenvolvimento.

## 🎯 Desenvolvedor focado em:

- Data Engineering
- Analytics
- R Programming
- Python Programming
- Automação de processos
- Engenharia de Software

## 📝 Contato
* Autor: Carlos da Costa
* Recife, PE - Brasil
* Telefone: +55 81 99712 9140
* Telegram: @jcarlossc
* Blogger linguagem R: https://informaticus77-r.blogspot.com/
* Blogger linguagem Python: https://informaticus77-python.blogspot.com/
* Email: jcarlossc1977@gmail.com
* LinkedIn: https://www.linkedin.com/in/carlos-da-costa-669252149/
* GitHub: https://github.com/jcarlossc
* Kaggle: https://www.kaggle.com/jcarlossc/
* Twitter/X: https://x.com/jcarlossc1977





