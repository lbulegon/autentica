# management/commands/meuprograma.py

from django.core.management.base import BaseCommand
import time
import logging
import os
import threading
import queue
from datetime import datetime, date
from motopro.models import TarefaConfig  # ajuste conforme o app

class Command(BaseCommand):
    help = 'Executa múltiplas tarefas residentes, configuráveis via Admin.'

    def handle(self, *args, **options):
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'meuprograma.log')

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self.stdout.write(self.style.SUCCESS('Programa residente iniciado, aguardando execuções configuráveis.'))

        message_queue = queue.Queue()

        def tarefa(tarefa_config, msg_queue):
            last_execution_date = None
            while True:
                # Recarrega status da tarefa no banco para verificar se foi ativada/desativada
                tarefa_atualizada = TarefaConfig.objects.get(id=tarefa_config.id)
                if not tarefa_atualizada.ativa:
                    time.sleep(10)
                    continue

                now = datetime.now()
                current_time = now.strftime('%H:%M')
                today = date.today()

                if current_time == tarefa_atualizada.horario and last_execution_date != today:
                    mensagem = f'Tarefa [{tarefa_atualizada.nome}] executada às {tarefa_atualizada.horario} no dia {today}'
                    msg_queue.put(mensagem)
                    logging.info(mensagem)

                    last_execution_date = today

                time.sleep(30)

        # Cria uma thread para cada TarefaConfig ativa
        tarefas = TarefaConfig.objects.all()
        threads = []

        for tarefa_config in tarefas:
            thread = threading.Thread(target=tarefa, args=(tarefa_config, message_queue), daemon=True)
            thread.start()
            threads.append(thread)

        try:
            while True:
                try:
                    mensagem = message_queue.get(timeout=1)
                    self.stdout.write(mensagem)
                except queue.Empty:
                    pass
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Programa interrompido manualmente.'))
