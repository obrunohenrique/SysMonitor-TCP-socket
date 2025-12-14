import pika 
import json
import time


HOST = 'localhost'
QUEUE_NAME = 'metricas_pc'


def main():
    # Estabelece conexao com o broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    print(f" [*] Servidor Middleware aguardando mensagens em '{QUEUE_NAME}'.")
    print(" [*] Pressione CTRL+C para sair.")


    def callback(ch, method, properties, body):
        mensagem = json.loads(body)

        # Simula o processamento/visualização
        print("\n" + "="*40)
        print(f" [x] Recebido dados de: {mensagem.get('id_cliente')}")
        print(f"     CPU Geral: {mensagem.get('cpu_geral')}%")
        print(f"     Memória Usada: {mensagem.get('mem_utilizada'):.2f} GB")
        print(f"     Delay de processamento: {time.time() - mensagem.get('timestamp'):.4f}s")
        print("="*40)

        # confirma para o rabbitmq que a mensagem foi processada com sucesso
        # Se nao confirmar, a mensagem volta pra fila
        ch.basic_ack(delivery_tag=method.delivery_tag)
    

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    # Inicia o loop de escuta
    try:
        channel.start_consuming()
    
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
        print("\nServidor encerrado")



if __name__ == '__main__':
    main()
