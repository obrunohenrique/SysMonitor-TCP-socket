import socket
import struct
import threading
import sys
import json
import time

HOST = '0.0.0.0'
PORT = 8080
BUFFER_SIZE = 1024
HEADER_SIZE = 4

estado_clientes = {}
clients_lock = threading.Lock()


def receive_all(sock, n):
    data = bytearray()

    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            return None
        data.extend(packet)
    return data


def monitor_display():
    while True:
        with clients_lock:
            # Cria uma cópia dos dados para não prender o lock por muito tempo
            dados_para_exibir = estado_clientes.copy() 

        print("\n" + "="*50)
        print("ESTADO ATUAL DO MONITORAMENTO DE CLIENTES")
        print("="*50)

        if not dados_para_exibir:
            print("Nenhum cliente conectado ou enviando dados.")
        else:
            for ip, dados in dados_para_exibir.items():
                print(f"[{ip}]")
                print(f"  CPU Geral: {dados.get('cpu_geral', 'N/A'):.2f}%")
                print(f"  CPU por Nucleo: {dados.get('cpu_por_nucleo', 'N/A')}%")
                print(f"  Memória Total: {dados.get('mem_total', 'N/A'):.2f} GB")
                print(f"  Memória Utilizada: {dados.get('mem_utilizada', 'N/A'):.2f} GB")
                print(f"  Memória Livre: {dados.get('mem_livre', 'N/A'):.2f} GB")
                print("-" * 20)

        # 3. Espera antes de atualizar a visualização
        time.sleep(10) # Atualiza a cada 10 segundos


def handle_client(connection, address):
    """Lida com as requisições do cliente conectado"""
    print(f'conectado por {address} (thread: {threading.current_thread().name})')

    try:

        while True:

            tamanho_bytes = receive_all(connection, HEADER_SIZE)
            
            if tamanho_bytes is None:
                break

            tamanho_mensagem = struct.unpack('>I', tamanho_bytes)[0]

            data = receive_all(connection, tamanho_mensagem)

            if data is None:
                break

            mensagem = data.decode('utf-8')
            dados_monitoramento = json.loads(mensagem)

            with clients_lock:
                estado_clientes[address[0]] = dados_monitoramento
            
            print(f"Dados atualizados para o cliente {address[0]}")
            

    except ConnectionError:
        print(f'Cliente {address} desconectou abruptamente.')
    except json.JSONDecodeError:
        print(f'Erro de JSON no cliente {address}. Dados corrompidos?')
    except Exception as e:
        print(f'Erro inesperado no handle_client {address}: {e}')
    finally:
        with clients_lock:
            #Remove o cliente ao fechar a conexao
            if address[0] in estado_clientes:
                del estado_clientes[address[0]]
                print(f'Cliente {address[0]} removido do estado.')
        connection.close()
        print(f'conexao com {address} encerrada. (Thread: {threading.current_thread().name}) finalizada)')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: 
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f'Bind falhou: {e}')
        sys.exit(1)

    server_socket.listen(5)
    print(f"Servidor Listening em: {HOST}:{PORT}")
    print('Aguardando novas conexões...')

    display_thread = threading.Thread(target=monitor_display, name='Display-Thread')
    display_thread.daemon = True
    display_thread.start()

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
