import socket
import sys

HOST = '192.168.1.7'
PORT = 8080
BUFFER_SIZE = 1024

#Cria o socket e estabelece conexão
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f'Conexao estabelecida')

#Ler e escrever na conexao
while True:
    mensagem = input("Digite sua mensagem > ")

    if len(mensagem) == 0:
        break

    client_socket.sendall(mensagem.encode('utf-8'))
    print(f'Enviado > {mensagem}')

    data = client_socket.recv(BUFFER_SIZE)

    if not data:
        break

    print(f'Recebido > {data.decode('utf-8')}')

#Passo 3: Fechar as conexoes
if client_socket:
    client_socket.close()
    print(f'Socket do cliente fechado!')

sys.close(0)
