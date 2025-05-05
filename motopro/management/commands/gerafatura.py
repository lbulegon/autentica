from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal
from datetime import date
from motopro.models import Vaga, Estabelecimento_Fatura, Estabelecimento_Contrato, Estabelecimento


class Command(BaseCommand):
    help = 'Gera faturas mensais por estabelecimento com base nas vagas utilizadas no mês corrente'

    def handle(self, *args, **kwargs):
        hoje = date.today()
        primeiro_dia_mes = hoje.replace(day=1)

        contratos_vigentes = Estabelecimento_Contrato.objects.filter(status="vigente")

        for contrato in contratos_vigentes:
            estabelecimento = contrato.estabelecimento

            vagas = Vaga.objects.filter(
                contrato=contrato,
                data_da_vaga__range=(primeiro_dia_mes, hoje),
                status="finalizada"
            )

            total_fixas   = vagas.filter(tipo_vaga='fixa').count()
            total_spot    = vagas.filter(tipo_vaga='spot').count()
            total_extra   = vagas.filter(tipo_vaga='extra').count()

            if total_fixas + total_spot + total_extra == 0:
                self.stdout.write(f"Sem vagas finalizadas para faturar em {estabelecimento.nome}")
                continue

            valor_fixa  = contrato.get_valor_item("valor_vaga_fixa") or Decimal("0.00")
            valor_spot  = contrato.get_valor_item("valor_vaga_spot") or Decimal("0.00")
            valor_extra = contrato.get_valor_item("valor_tele_extra") or Decimal("0.00")

            valor_total = (
                (total_fixas * valor_fixa) +
                (total_spot * valor_spot) +
                (total_extra * valor_extra)
            )

            fatura, criada = Estabelecimento_Fatura.objects.get_or_create(
                estabelecimento=estabelecimento,
                data_referencia=primeiro_dia_mes,
                defaults={
                    'valor_total': valor_total,
                    'status': 'aberta',
                    'quantidade_alocacoes': total_fixas + total_spot + total_extra
                }
            )

            if not criada:
                fatura.valor_total = valor_total
                fatura.quantidade_alocacoes = total_fixas + total_spot + total_extra
                fatura.save()

            self.stdout.write(
                f"{'Criada' if criada else 'Atualizada'} fatura para {estabelecimento.nome}: "
                f"{total_fixas} fixas, {total_spot} spot, {total_extra} extra | "
                f"Total: R$ {valor_total:.2f}"
            )
