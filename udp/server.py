import socket
import threading
import sys
import json
import time

HOST = '0.0.0.0'
PORT = 8080
BUFFER_SIZE = 4096 

estado_clientes = {}
clients_lock = threading.Lock()
TIMEOUT_CLIENTE = 15

def monitor_display():
    while True:
        with clients_lock:
            agora = time.time()
            ips_para_remover = []

            for ip, dados in estado_clientes.items():
                ultima_atualizacao = dados.get('last_seen', 0)
                if agora - ultima_atualizacao > TIMEOUT_CLIENTE:
                    ips_para_remover.append(ip)

            for ip in ips_para_remover:
                del estado_clientes[ip]
                print(f"\n[Monitor] Cliente {ip} removido por inatividade (Timeout).")

            dados_para_exibir = estado_clientes.copy()

        print("\n" + "="*50)
        print("ESTADO ATUAL DO MONITORAMENTO DE CLIENTES (UDP)")
        print("="*50)

        if not dados_para_exibir:
            print("Nenhum cliente ativo detectado.")
        else:
            for ip, dados in dados_para_exibir.items():
                print(f"[{ip}] (Último sinal: {time.time() - dados['last_seen']:.1f}s atrás)")
                print(f"  CPU Geral: {dados.get('cpu_geral', 'N/A'):.2f}%")
                print(f"  CPU por Nucleo: {dados.get('cpu_por_nucleo', 'N/A')}%")
                print(f"  Memória Total: {dados.get('mem_total', 'N/A'):.2f} GB")
                print(f"  Memória Utilizada: {dados.get('mem_utilizada', 'N/A'):.2f} GB")
                print(f"  Memória Livre: {dados.get('mem_livre', 'N/A'):.2f} GB")
                print("-" * 20)

        time.sleep(5)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try: 
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f'Bind falhou: {e}')
        sys.exit(1)

    print(f"Servidor UDP ouvindo em: {HOST}:{PORT}")

    display_thread = threading.Thread(target=monitor_display, name='Display-Thread')
    display_thread.daemon = True
    display_thread.start()

    while True:
        try:
            data, address = server_socket.recvfrom(BUFFER_SIZE)

            mensagem = data.decode('utf-8')
            
            try:
                dados_monitoramento = json.loads(mensagem)
                
                dados_monitoramento['last_seen'] = time.time()

                with clients_lock:
                    estado_clientes[address[0]] = dados_monitoramento
                
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON de {address[0]}")

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