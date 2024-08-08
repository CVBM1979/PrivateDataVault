# PrivateDataVault

## Descrição

Este projeto é uma aplicação web desenvolvida em Flask que permite gerenciar arquivos em um repositório GitHub. A aplicação fornece funcionalidades para fazer upload, download e deletar arquivos no repositório.

## Funcionalidades

- Upload de arquivos para um repositório GitHub
- Download de arquivos do repositório GitHub
- Deleção de arquivos do repositório GitHub

## Estrutura do Projeto

PrivateDataVault/
├── .gitignore
├── .env.example
├── README.md
├── app.py
├── build_executable.py
├── MyFlaskApp.spec
├── requirements.txt
├── script.js
├── index.html
└── dist/

## Requisitos

- Python 3.9 ou superior
- Git

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/CVBM1979/PrivateDataVault.git
cd PrivateDataVault

### 2. Configurar o arquivo .env

Crie um arquivo .env e insira o seu GITHUB_TOKEN:
GITHUB_TOKEN=seu_github_token

### 3. Instalar as dependências

python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install -r requirements.txt


### 4. Criar o executável

pyinstaller MyFlaskApp.spec

### 5. Executar o executável

dist/MyFlaskApp/MyFlaskApp.exe > output.log 2>&1

### 6. Acessar a aplicação

index.html
