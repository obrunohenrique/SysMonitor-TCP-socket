import socket
import threading
import sys
import time 

HOST = '192.168.1.7'
PORT = 8080
BUFFER_SIZE = 1024

def handle_client(connection, address):
    """Lida com as requisições do cliente conectado"""
    print(f'conectado por {address} (thread: {threading.current_thread().name})')

    try:

        while True:

            data = connection.recv(BUFFER_SIZE)
            
            if not data:
                break

            mensagem = data.decode('utf-8')
            print(f'[{address[1]}] Recebido > {mensagem}')

            resposta = mensagem.upper()

            time.sleep(0.1)

            connection.sendall(resposta.encode('utf-8'))
            print(f'[{address[1]}] Enviado > {resposta}')

    except ConnectionError:
        print(f'Cliente {address} desconectou abruptamente.')
    finally:
        connection.close()
        print(f'conexao com {address} encerrada. (Thread: {threading.current_thread().name}) finalizada)')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: 
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f'Bind falhou: {e}')
        sys.close(1)

    server_socket.listen(5)
    print(f"Servidor Listening em: {HOST}:{PORT}")
    print('Aguardando novas conexões...')

    #while externo pra voltar sempre pro accept para esperar novas conexões
    while True:
        try:
            connection, address = server_socket.accept()

            #Crio uma thread e direciono a conexao pra ela
            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, address),
                name=f'Client-{address[1]}'
            )
            client_thread.daemon = True #programa principal sai mesmo com threads rodando
            client_thread.start()

            # volta imediatamente para o accept

        except KeyboardInterrupt:
            print("\nServidor encerrado por usuario")
            break
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            continue

    server_socket.close()
    print('Socket do servidor fechado!')


if __name__ == "__main__":
    start_server()