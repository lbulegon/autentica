from django.core.management.base import BaseCommand
from django.utils import timezone
from motopro.models import estabelecimentocontrato, vaga

class Command(BaseCommand):
    help = 'Cria vagas individuais para motoboys com base nos contratos dos estabelecimentos'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        contratos = estabelecimentocontrato.objects.all()

        for contrato in contratos:
            vagas_existentes = vaga.objects.filter(
                estabelecimento=contrato.estabelecimento,
                contrato=contrato,
                data_da_vaga=hoje
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
                    contrato=contrato,
                    data_da_vaga=hoje,
                  
                )

            self.stdout.write(
                f'{vagas_para_criar} vaga(s) criada(s) para {contrato.estabelecimento.nome} - {contrato.get_turno_display()}'
            )
