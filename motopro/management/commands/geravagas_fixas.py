from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from motopro.models import Estabelecimento_Contrato, Vaga

class Command(BaseCommand):
    help = 'Cria vagas fixas diárias (dia e noite) com base nos contratos vigentes dos estabelecimentos'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        contratos = Estabelecimento_Contrato.objects.filter(status="vigente")

        for contrato in contratos:
            if contrato.data_inicio and contrato.data_inicio > hoje:
                continue
            if contrato.data_fim and contrato.data_fim < hoje:
                continue

            periodos = {
                "dia":   (time(8, 0), time(18, 0)),
                "noite": (time(18, 0), time(1, 0)),  # até 1h da manhã
            }

            for chave, (hora_inicio, hora_fim) in periodos.items():
                item_vagas = contrato.itens.filter(item__chave_sistema=f"max_vagas_fixas_{chave}").first()

                if not item_vagas:
                    self.stdout.write(f'Contrato sem item "max_vagas_fixas_{chave}" para {contrato.estabelecimento.nome}')
                    continue

                try:
                    quantidade_vagas = int(item_vagas.valor)
                except ValueError:
                    self.stdout.write(f'Valor inválido para "max_vagas_fixas_{chave}" no contrato de {contrato.estabelecimento.nome}')
                    continue

                vagas_existentes = Vaga.objects.filter(
                    contrato           = contrato,
                    data_da_vaga       = hoje,
                    hora_inicio_padrao = hora_inicio,
                    hora_fim_padrao    = hora_fim,
                    tipo_vaga          = 'fixa'
                ).count()

                if vagas_existentes >= quantidade_vagas:
                    self.stdout.write(
                        f'Vagas já lançadas ({chave}): {contrato.estabelecimento.nome}'
                    )
                    continue

                vagas_para_criar = quantidade_vagas - vagas_existentes

                for _ in range(vagas_para_criar):
                    Vaga.objects.create(
                        contrato           = contrato,
                        data_da_vaga       = hoje,
                        hora_inicio_padrao = hora_inicio,
                        hora_fim_padrao    = hora_fim,
                        tipo_vaga          = 'fixa'
                    )

                self.stdout.write(
                    f'{vagas_para_criar} vaga(s) criada(s) para {contrato.estabelecimento.nome} ({chave})'
                )
