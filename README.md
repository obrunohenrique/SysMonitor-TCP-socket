## 📘 Monitoring System – TCP Client/Server

This project implements a simple performance-monitoring system using TCP sockets.
Multiple machines can run the client, which collects CPU and memory metrics and sends them to a central server that displays the data in near real-time.

## 📂 Project Structure

```
/monitoring
│── server.py   # TCP server that receives and displays metrics
│── client.py   # Client that collects and sends metrics
│── README.md 
```

## 🚀 1. Requirements

Before running the project, make sure you have:

### 🐍 Python 3.8+

Check your version:

```
python --version
```

### 📦 Required Libraries

The client uses the psutil library to collect system metrics:

```
pip install -r requirements.txt
```

The server uses only Python’s standard library.

## 🌐 2. Network Setup

The system works on:

- Local network (LAN)
- Wi-Fi / Ethernet
- Multiple machines
- A single machine (localhost testing)

### 🔍 Get the Server's IP Address

You MUST use the IP of the computer running server.py.

On Windows:
```
ipconfig
```

Look for:
```
IPv4 Address . . . : 192.168.x.x
```

On Linux / macOS:
```
ip a
```

or
```
ifconfig
```

Use the IP belonging to your active network interface.

## 🖥️ 3. Running the Server

The server is configured to accept connections from any device in the LAN:

```
HOST = "0.0.0.0"
PORT = 8080
```

▶ Start the server:
```
python server.py
```

You should see:

```
Servidor Listening em: 0.0.0.0:8080
Aguardando novas conexões...
```

The server automatically displays updated metrics every 10 seconds, including:

- Client IP
- CPU usage (overall + per core)
- Memory total / used / free

## 💻 4. Configuring and Running the Client

Inside client.py, replace:

```
HOST = "Coloque o IP do Servidor"
```

with the actual server IP, for example:

```
HOST = "192.168.x.x"
```

The port remains:

```
PORT = 8080
```

▶ Start the client:
```
python client.py
```

Expected output:

```
Conexao estabelecida com 192.168.x.x:8080
Dados enviados: 221 bytes.
```

The client automatically sends metrics every 5 seconds.

## 🔄 5. Running Multiple Clients (Same LAN)

Simply:

Put the server’s IP in each client.

Run client.py on each machine.

The server will show entries like:

```
[192.168.1.10]
  CPU Total: ...
  Memory: ...

[192.168.1.11]
  CPU Total: ...
  Memory: ...
```

## 🛑 6. Common Errors & Fixes

| Error                   | Cause                   | Solution                     |
|-------------------------|--------------------------|------------------------------|
| `ConnectionRefusedError` | Server not running       | Start `server.py` first      |
| No data on server       | Wrong IP                 | Check with `ipconfig / ip a` |
| Client stuck            | Firewall blocked         | Allow port 8080              |
| JSON decode error       | Corrupted transmission   | Restart client               |



## 🧹 7. Stopping the System

Stop server: `Ctrl + C`

Stop client: `Ctrl + C`

Both scripts close sockets gracefully.
