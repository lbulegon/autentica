from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.db.models import Sum

from motopro.models import Motoboy, Motoboy_Adiantamento

class Command(BaseCommand):
    help = 'Gera repasses semanais para motoboys com base nas bandas utilizadas e valores pagos'

    def add_arguments(self, parser):
        parser.add_argument('--inicio', type=str, help='Data de início no formato YYYY-MM-DD')
        parser.add_argument('--fim', type=str, help='Data de fim no formato YYYY-MM-DD')

    def handle(self, *args, **options):
        inicio_str = options['inicio']
        fim_str = options['fim']

        hoje = date.today()
        data_fim = datetime.strptime(fim_str, "%Y-%m-%d").date() if fim_str else hoje
        data_inicio = datetime.strptime(inicio_str, "%Y-%m-%d").date() if inicio_str else data_fim - timedelta(days=6)

        self.stdout.write(self.style.NOTICE(f"Calculando repasses de {data_inicio} até {data_fim}"))

        motoboys = Motoboy.objects.all()
        total_geral = Decimal('0.00')
        repasses_criados = 0

        for motoboy in motoboys:
            alocacoes = motoboy.motoboy_alocacao_set.filter(vaga__data_da_vaga__range=(data_inicio, data_fim))
            valor_bruto = Decimal('0.00')

            for aloc in alocacoes:
                contrato = aloc.vaga.contrato
                for banda in aloc.bandas.all():
                    chave = f"faixa_km_{banda.faixa_km}"
                    valor_km = contrato.get_valor_item(chave) or Decimal('0.00')
                    valor_bruto += valor_km * banda.quantidade

            valor_ja_repassado = Motoboy_Adiantamento.objects.filter(
                motoboy=motoboy,
                data_referencia__range=(data_inicio, data_fim)
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

            valor_final = valor_bruto - valor_ja_repassado

            if valor_final > 0:
                Motoboy_Adiantamento.objects.create(
                    motoboy=motoboy,
                    data_referencia=data_fim,
                    valor=valor_final,
                    tipo_repasse='fixo',
                    observacao=f"Repasse semanal automático ({data_inicio} a {data_fim})"
                )
                self.stdout.write(self.style.SUCCESS(f"✓ {motoboy.nome}: R$ {valor_final:.2f}"))
                total_geral += valor_final
                repasses_criados += 1

        if repasses_criados == 0:
            self.stdout.write(self.style.WARNING("Nenhum repasse necessário."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Total repassado: R$ {total_geral:.2f}"))
