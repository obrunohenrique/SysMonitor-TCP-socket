import socket
import struct
import sys
import psutil
import json
import time

HOST = '192.168.1.7'
PORT = 8080

try:
    #Cria o socket e estabelece conexão
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f'Conexao estabelecida com {HOST}:{PORT}')

    #Ler e escrever na conexao
    while True:
        cpu_geral = psutil.cpu_percent(interval=1)
        cpu_por_nucleo = psutil.cpu_percent(interval=1, percpu=True)

        mem= psutil.virtual_memory()
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
        tamanho_mensagem = len(mensagem_bytes)

        prefixo_tamanho = struct.pack('>I', tamanho_mensagem)

        client_socket.sendall(prefixo_tamanho + mensagem_bytes)
        print(f'Dados enviados: {tamanho_mensagem} bytes.')

        time.sleep(5)

except ConnectionRefusedError:
    print(f"ERRO: conexao recusada. O servidor pode nao estar ativo em {HOST}:{PORT}.")
except KeyboardInterrupt:
    print(f'\nCliente encerrado pelo usuario')
except Exception as e:
    print(f"Um erro ocorreu: {e}")

finally:
    #Passo 3: Fechar as conexoes
    if client_socket:
        client_socket.close()
        print(f'Socket do cliente fechado!')

    sys.exit(0)
