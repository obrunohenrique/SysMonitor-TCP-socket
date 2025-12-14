import pika
import psutil
import json
import time
import socket

HOST = 'localhost' 
QUEUE_NAME = 'metricas_pc'


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    print(f" [!] Agente iniciado. Enviando para fila '{QUEUE_NAME}'...")

    hostname = socket.gethostname()

    while True:

        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_used_gb = mem.used / (1024 ** 3)

        payload = {
            'id_cliente': hostname,
            'cpu_geral': cpu,
            'mem_utilizada': mem_used_gb,
            'timestamp': time.time()
        }

        mensagem_json = json.dumps(payload)

        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=mensagem_json,
            properties=pika.BasicProperties(delivery_mode=1) # torna a mensagem NAO persistente
        )

        print(f" [X] Enviado métrica: CPU {cpu}%")


        time.sleep(4)

except KeyboardInterrupt:
    print("Encerrando agente")
    connection.close()
    