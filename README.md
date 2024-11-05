# FitLife

[FitLife](https://fitlife-production.up.railway.app/)

## Descrição

FitLife é uma aplicação web desenvolvida para ajudar os usuários a gerenciar seus treinos e acompanhar seu progresso físico. A plataforma oferece funcionalidades como criação de treinos, acompanhamento de exercícios, e gestão de perfis de usuário.

## Funcionalidades

- **Autenticação de Usuário**: Cadastro, login e logout de usuários.
- **Gestão de Perfis**: Atualização de informações pessoais e preferências.
- **Criação de Treinos**: Permite aos usuários criar e personalizar seus treinos.
- **Acompanhamento de Exercícios**: Registro e monitoramento de exercícios realizados.
- **Administração**: Interface de administração para gerenciar usuários e conteúdos.

## Tecnologias Utilizadas

### Backend

- **Django**: Framework web utilizado para construir a aplicação.
- **Django-Cotton**: Biblioteca para criar componentes reutilizáveis nas templates do Django.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar dados da aplicação.

### Frontend

- **HTMX**: biblioteca JavaScript que permite adicionar interatividade avançada ao HTML usando apenas atributos.
- **Alpine.js**: Framework JavaScript para adicionar interatividade ao HTML.
- **Bootstrap**: Framework CSS para estilização de componentes.
- **LESS**: Pré-processador CSS para facilitar a escrita de estilos.

## Estrutura do Projeto

- **apps/**: Contém os aplicativos Django da aplicação.
  - **core/**: Funcionalidades centrais e utilitários.
  - **users/**: Gestão de usuários e autenticação.
  - **gym/**: Funcionalidades relacionadas a treinos e exercícios.
- **config/**: Configurações do projeto Django.
- **templates/**: Templates HTML utilizados na aplicação.
- **static/**: Arquivos estáticos como CSS, JavaScript e imagens.
- **tests/**: Testes automatizados para a aplicação.

## Como Executar

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/fitlife.git
    cd fitlife
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```sh
    poetry install
    ```

4. Configure as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto e adicione as variáveis necessárias, como `SECRET_KEY` e `DEBUG`.

5. Execute as migrações do banco de dados:
    ```sh
    python manage.py migrate
    ```

6. Inicie o servidor de desenvolvimento:
    ```sh
    python manage.py runserver
    ```