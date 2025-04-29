from django.core.management.base import BaseCommand
from motopro.models import estabelecimentocontrato
from motopro.models import VagaSlot
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Gera automaticamente vagasSpot para os contratos ativos em uma data.'

    def add_arguments(self, parser):
        parser.add_argument('data', type=str, help='Data no formato YYYY-MM-DD')

    def handle(self, *args, **options):
        data_str = options['data']
        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            self.stderr.write(self.style.ERROR("Formato de data inválido. Use YYYY-MM-DD."))
            return

        contratos = estabelecimentocontrato.objects.all()

        total_vagas_criadas = 0

        for contrato in contratos:
            quantidade = contrato.quantidade_vagas
            hora_inicio = contrato.horario_inicio
            hora_fim = contrato.horario_fim

            duracao_turno = (
                datetime.combine(datetime.today(), hora_fim) -
                datetime.combine(datetime.today(), hora_inicio)
            )

            if duracao_turno.total_seconds() <= 0:
                self.stderr.write(self.style.WARNING(
                    f"Contrato {contrato.id} ignorado: horário inválido."))
                continue

            intervalo = duracao_turno / quantidade

            for i in range(quantidade):
                inicio_slot = (datetime.combine(datetime.today(), hora_inicio) + intervalo * i).time()
                fim_slot = (datetime.combine(datetime.today(), hora_inicio) + intervalo * (i + 1)).time()

                slot, created = VagaSlot.objects.get_or_create(
                    contrato=contrato,
                    data=data,
                    hora_inicio=inicio_slot,
                    hora_fim=fim_slot,
                )
                if created:
                    total_vagas_criadas += 1

        self.stdout.write(self.style.SUCCESS(f'{total_vagas_criadas} vagasSpot criadas para {data}.'))
