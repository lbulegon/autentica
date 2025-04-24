# seu_app/management/commands/escanear_portas.py

import socket
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Faz uma varredura de portas abertas em um host'

    def add_arguments(self, parser):
        parser.add_argument('--host', type=str, required=True, help='IP ou hostname do alvo')
        parser.add_argument('--inicio', type=int, default=20, help='Porta inicial')
        parser.add_argument('--fim', type=int, default=1024, help='Porta final')

    def handle(self, *args, **options):
        host = options['host']
        porta_inicial = options['inicio']
        porta_final = options['fim']

        self.stdout.write(self.style.SUCCESS(f"Iniciando escaneamento em {host} (portas {porta_inicial}-{porta_final})"))

        for porta in range(porta_inicial, porta_final + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            resultado = sock.connect_ex((host, porta))
            if resultado == 0:
                self.stdout.write(self.style.SUCCESS(f"Porta {porta}: ABERTA"))
            else:
                self.stdout.write(self.style.NOTICE(f"Porta {porta}: FECHADA"))
            sock.close()

        self.stdout.write(self.style.SUCCESS("Escaneamento finalizado."))
