# Pong Multiplayer
Projeto com intuito de desenvolver uma versão simplicada do jogo Pong utilizando sockets. Este 
projeto tem como objetivo simular um sistema distribuito para obtenção de nota de trabalho na matéria de 
Sistemas Distribuidos.

## Requisitos:
- python 3.6+
- virtualenv

## Setup:

**Instalar o virtualenv (se não estiver instalado):**
```bash
pip install virtualenv  # pip
pip3 install virtualenv  # pip3
sudo apt-get install virtualenv  # linux (ie: Ubuntu20-04)
```
### Na pasta principal do projeto executar os seguintes passos:

**Criar o virtualenv:**
```bash
virtualenv venv
```

**Entrar na virtualenv:**
```bash
source venv/bin/activate  # linux
venv\Scripts\activate  # windows
```

**Instalar dependências:**
```bash
pip install -r requirements.txt  # pip
pip install -r requirements.txt  # pip3
```

## Uso:

**Iniciar Servidor:**
```bash
python main.py start-server
```

**Iniciar jogador 1:**
```bash
python run-game.py
```

**Iniciar jogador 2:**
```bash
python run-game.py
```

## Dupla
Jadson Lucio
Francisco Neto

## Contribuições:
Fique a vontade para contribuir :)

## Lincença:
Em breve...
