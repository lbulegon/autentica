from django.core.management.base import BaseCommand
from django.utils import timezone
from motopro.models import Estabelecimento_Contrato, Vaga

class Command(BaseCommand):
    help = 'Cria vaga avulsa (spot) para contratos que permitem vaga spot'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()

        contratos = Estabelecimento_Contrato.objects.filter(
            status='vigente',
            itens__item__chave_sistema='permite_vaga_spot'
        ).distinct()

        for contrato in contratos:
            if contrato.data_inicio and contrato.data_inicio > hoje:
                continue
            if contrato.data_fim and contrato.data_fim < hoje:
                continue

            vaga_existente = Vaga.objects.filter(
                contrato=contrato,
                data_da_vaga=hoje,
                tipo_vaga='spot'
            ).exists()

            if vaga_existente:
                self.stdout.write(f'Vaga spot já existe para {contrato.estabelecimento.nome} em {hoje}')
                continue

            Vaga.objects.create(
                contrato=contrato,
                tipo_vaga='spot',
                data_da_vaga=hoje,
                hora_inicio_padrao='10:30',  # ajuste se quiser horário diferente
                hora_fim_padrao='18:00',     # ajuste se quiser horário diferente
                status='aberta'
            )

            self.stdout.write(f'Vaga spot criada para {contrato.estabelecimento.nome} em {hoje}')
