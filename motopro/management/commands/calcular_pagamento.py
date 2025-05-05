from django.core.management.base import BaseCommand
from django.db.models import Q
from datetime import datetime
from motopro.models import Vaga, Motoboy_Alocacao, Motoboy, Estabelecimento
from motopro.utils import calcular_pagamento  # sua função utilitária

class Command(BaseCommand):
    help = 'Calcula os pagamentos de todos os motoboys alocados entre duas datas'

    def add_arguments(self, parser):
        parser.add_argument('inicio', type=str, help='Data de início (YYYY-MM-DD)')
        parser.add_argument('fim', type=str, help='Data de fim (YYYY-MM-DD)')

    def handle(self, *args, **options):
        inicio = datetime.strptime(options['inicio'], '%Y-%m-%d').date()
        fim = datetime.strptime(options['fim'], '%Y-%m-%d').date()

        alocacoes = Motoboy_Alocacao.objects.filter(
            vaga__data_da_vaga__range=(inicio, fim)
        ).select_related(
            'motoboy',
            'vaga__contrato__estabelecimento'
        )

        pagamentos = {}

        for aloc in alocacoes:
            motoboy = aloc.motoboy
            estabelecimento = aloc.vaga.contrato.estabelecimento

            if not estabelecimento:
                continue  # pula se não houver estabelecimento vinculado

            chave = (motoboy.id, estabelecimento.id)
            if chave not in pagamentos:
                pagamentos[chave] = calcular_pagamento(estabelecimento, motoboy, inicio, fim)

        for (motoboy_id, est_id), pagamento in pagamentos.items():
            self.stdout.write(self.style.SUCCESS(
                f"{pagamento['motoboy']} | {pagamento['estabelecimento']} | "
                f"Recebe: R${pagamento['total_motoboy_recebe']}"
            ))
