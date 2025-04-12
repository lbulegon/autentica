# core/management/commands/criar_vagas_turnos.py

from django.core.management.base import BaseCommand
from datetime import date
from motopro.models import estabelecimentocontrato, vaga
from django.utils import timezone

class Command(BaseCommand):
    help = 'Cria vagas individuais para motoboys com base nos contratos dos estabelecimentos'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
    
        contratos = estabelecimentocontrato.objects.all()

        for contrato in contratos:
            # Verifica se já existem vagas criadas para esse contrato no dia
            vagas_existentes = vaga.objects.filter(
                estabelecimento=contrato.estabelecimento,
                data_da_vaga=hoje,              
            ).count()

            if vagas_existentes >= contrato.quantidade_vagas:
                self.stdout.write(
                    f'Vagas já lançadas: {contrato.estabelecimento.nome} | {contrato.get_turno_display()}'
                )
                continue

            vagas_para_criar = contrato.quantidade_vagas - vagas_existentes

            for _ in range(vagas_para_criar):
                vaga.objects.create(
                    estabelecimento=contrato.estabelecimento,
                    data_da_vaga=hoje
                )

            self.stdout.write(
                f'{vagas_para_criar} vaga(s) criada(s) para {contrato.estabelecimento.nome} - {contrato.get_turno_display()}'
            )
