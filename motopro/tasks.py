# motopro/tasks.py
from celery import shared_task
import time
import logging

@shared_task
def tarefa_residente(mensagem='Executando tarefa residente...', intervalo=5, vezes=None):
    count = 0
    log_file = '/tmp/meuprograma.log'
    logging.basicConfig(filename=log_file, level=logging.INFO)

    while True:
        logging.info(mensagem)
        print(mensagem)
        time.sleep(intervalo)
        count += 1
        if vezes is not None and count >= vezes:
            break
