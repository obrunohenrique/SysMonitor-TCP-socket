import socket
import sys
import psutil
import json
import time

HOST = '192.168.1.3'
PORT = 8080

client_socket = None

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'Cliente UDP iniciado. Alvo: {HOST}:{PORT}')

    while True:
        cpu_geral = psutil.cpu_percent(interval=1)
        cpu_por_nucleo = psutil.cpu_percent(interval=1, percpu=True)

        mem = psutil.virtual_memory()
        mem_total = mem.total / (1024 ** 3)
        mem_utilizada = mem.used / (1024 ** 3)
        mem_livre = mem.free / (1024 ** 3)

        data = {
            'cpu_geral': cpu_geral,
            'cpu_por_nucleo': cpu_por_nucleo,
            'mem_total': mem_total,
            'mem_utilizada': mem_utilizada,
            'mem_livre': mem_livre
        }

        mensagem_bytes = json.dumps(data).encode('utf-8')
        
        client_socket.sendto(mensagem_bytes, (HOST, PORT))
        
        print(f'Pacote UDP enviado: {len(mensagem_bytes)} bytes.')

        time.sleep(5)

except KeyboardInterrupt:
    print(f'\nCliente encerrado pelo usuario')
except Exception as e:
    print(f"Um erro ocorreu: {e}")

finally:
    if client_socket:
        client_socket.close()
        print(f'Socket do cliente fechado!')

    sys.exit(0)