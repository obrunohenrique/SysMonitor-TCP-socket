# SysMonitor: Socket & Middleware Architectures

Este projeto é um sistema de monitoramento de performance (CPU e Memória RAM) desenvolvido em Python. O objetivo principal deste repositório é demonstrar e comparar três arquiteturas de comunicação distintas para sistemas distribuídos: **TCP**, **UDP** e **Middleware (Message Broker)**.

A aplicação consiste em agentes (Clientes) que coletam métricas da máquina local e as enviam para um monitor central (Servidor).

## 📂 Estrutura do Projeto

O projeto está organizado em módulos independentes:

- **`tcp/`**: Implementação usando Sockets TCP (Conexão persistente/Stream).
- **`udp/`**: Implementação usando Sockets UDP (Datagramas/Fire-and-forget).
- **`middleware/`**: Implementação desacoplada usando RabbitMQ (Padrão Pub/Sub).

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Psutil** (Coleta de métricas de hardware)
- **Socket** (Biblioteca padrão para TCP/UDP)
- **Pika** (Cliente Python para RabbitMQ)
- **Docker** (Para execução do servidor RabbitMQ)

---

## 🚀 Guia de Instalação

### 1. Clone o repositório
```
git clone [https://github.com/obrunohenrique/SysMonitor-socket-and-middleware.git](https://github.com/obrunohenrique/SysMonitor-socket-and-middleware.git)
cd SysMonitor-socket-and-middleware
```

### 2. Configure o Ambiente Virtual

(É recomendado usar um ambiente virtual para isolar as dependências).
```
Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as Dependências

```pip install -r requirements.txt```


### 💻 Como Rodar as Implementações?
Abra dois terminais: um para rodar o Servidor e outro para o Cliente. Certifique-se de que o ambiente virtual (.venv) esteja ativado em ambos.

#### 1. Implementação TCP (Confiabilidade)
Nesta versão, o cliente estabelece uma conexão dedicada com o servidor.
```
# Terminal 1 (Servidor)
cd tcp
python server.py

# Terminal 2 (Cliente)
cd tcp
python client.py
```

#### 2. Implementação UDP (Velocidade)
Nesta versão, os dados são enviados sem garantia de entrega ou conexão estabelecida, priorizando a velocidade.
```
# Terminal 1 (Servidor)
cd udp
python server.py

# Terminal 2 (Cliente)
cd udp
python client.py
```

#### 3. Implementação Middleware (Escalabilidade)

Esta versão utiliza o RabbitMQ para desacoplar o cliente do servidor.

Passo 1: Subir o RabbitMQ (Requer Docker)
```
docker run -d --name rabbitmq-monitor -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
(Opcional: Acesse http://localhost:15672 para ver o painel visual. Login: guest / Senha: guest)


Passo 2: Rodar os Scripts
```
# Terminal 1 (Servidor/Subscriber)
cd middleware
python server.py

# Terminal 2 (Cliente/Publisher)
cd middleware
python client.py
```
