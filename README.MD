# Sistema Bancário em Python com MySQL

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-green)

## 📖 Sobre o Projeto

Este projeto é uma simulação de um sistema bancário simples, desenvolvido em Python como um exercício prático de Programação Orientada a Objetos e integração com bancos de dados relacionais. A aplicação, que originalmente operava apenas em memória, foi refatorada para utilizar um banco de dados MySQL, garantindo a persistência e a integridade dos dados.

O sistema permite a criação de clientes, contas e a realização de operações financeiras básicas, servindo como um portfólio prático de habilidades de desenvolvimento back-end.

## ✨ Funcionalidades

-   **Gestão de Clientes:** Cadastro de novos clientes no sistema.
-   **Gestão de Contas:** Abertura de contas correntes vinculadas a um cliente.
-   **Operações Bancárias:**
    -   Realização de **Depósitos**.
    -   Realização de **Saques**, com validação de saldo, limite e número de saques.
-   **Consultas:**
    -   Exibição de **Extrato** detalhado com todo o histórico de transações.
    -   **Listagem** de todas as contas cadastradas com os dados dos seus titulares.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Banco de Dados:** MySQL
-   **Conector:** `mysql-connector-python`
-   **Controle de Versão:** Git & GitHub

## 🏛️ Arquitetura do Código

O projeto foi refatorado de um script único para uma estrutura modular, separando as responsabilidades:

-   **`main.py`**: Contém a lógica de execução principal e a interface com o usuário (menu).
-   **`database.py`**: Módulo responsável por gerenciar a conexão com o banco de dados.
-   **`config.py`**: Arquivo de configuração para armazenar dados sensíveis (senha do banco), ignorado pelo Git.
-   **`modelos/`**: Pacote contendo as classes que representam as entidades do sistema (Cliente, Conta, Transacao), seguindo os princípios de POO.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o projeto em sua máquina local.

### Pré-requisitos

-   Python 3.x
-   MySQL Server
-   Git (opcional, para clonar)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd SISTEMA_BANCARIO
    ```

2.  **Instale as dependências:**
    ```bash
    pip install mysql-connector-python
    ```

3.  **Configure o Banco de Dados:**
    -   Certifique-se de que seu servidor MySQL está rodando.
    -   Crie um schema (banco de dados) com o nome `mydb` (ou o nome que você usou). Você pode usar o MySQL Workbench para isso.
    -   Execute o script SQL para criar as tabelas. (Você pode gerar esse script no Workbench indo em `Database > Forward Engineer...`). É uma boa prática salvar esse script em um arquivo como `schema.sql` e adicioná-lo ao seu repositório.

4.  **Configure a Senha:**
    -   Na raiz do projeto, crie um arquivo chamado `config.py`.
    -   Dentro dele, adicione sua senha do banco de dados:
        ```python
        # config.py
        DB_PASSWORD = "sua_senha_aqui"
        ```
    -   Este arquivo não será enviado para o repositório, pois está listado no `.gitignore`.

5.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```

## 👨‍💻 Autor

-   **[Leonardo José]**
-   **LinkedIn:** [www.linkedin.com/in/leonardo-jnss]
-   **GitHub:** [https://github.com/Leonardojnss]