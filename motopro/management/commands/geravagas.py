from django.core.management.base import BaseCommand
from django.utils import timezone
from motopro.models import estabelecimentocontrato, vaga

class Command(BaseCommand):
    help = 'Cria vagas diárias com base nos contratos vigentes dos estabelecimentos'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        contratos = estabelecimentocontrato.objects.filter(status="vigente")

        for contrato in contratos:
            # Verifica se a data atual está dentro do período de vigência do contrato (se houver)
            if contrato.data_inicio and contrato.data_inicio > hoje:
                continue
            if contrato.data_fim and contrato.data_fim < hoje:
                continue

            vagas_existentes = vaga.objects.filter(
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
                    contrato=contrato,
                    data_da_vaga=hoje
                )

            self.stdout.write(
                f'{vagas_para_criar} vaga(s) criada(s) para {contrato.estabelecimento.nome} - {contrato.get_turno_display()}'
            )
