from datetime import timedelta, date
from decimal import Decimal
from django.db.models import Sum

from motopro.models import Motoboy, Motoboy_Adiantamento

def calcular_repasse_por_bandas(alocacao):
    contrato = alocacao.vaga.contrato
    total = Decimal('0.00')
    for banda in alocacao.bandas.all():
        chave = f"faixa_km_{banda.faixa_km}"
        valor = contrato.get_valor_item(chave) or Decimal('0.00')
        total += valor * banda.quantidade
    return total

def gerar_repasses_semanais(data_inicio=None, data_fim=None):
    hoje = date.today()
    data_fim = data_fim or hoje
    data_inicio = data_inicio or (data_fim - timedelta(days=6))

    resultado = []
    motoboys = Motoboy.objects.all()

    for motoboy in motoboys:
        alocacoes = motoboy.motoboy_alocacao_set.filter(vaga__data_da_vaga__range=(data_inicio, data_fim))

        valor_bruto = sum([calcular_repasse_por_bandas(aloc) for aloc in alocacoes], Decimal('0.00'))

        valor_ja_pago = Motoboy_Adiantamento.objects.filter(
            motoboy=motoboy,
            data_referencia__range=(data_inicio, data_fim)
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

        valor_final = valor_bruto - valor_ja_pago

        if valor_final > 0:
            Motoboy_Adiantamento.objects.create(
                motoboy=motoboy,
                data_referencia=data_fim,
                valor=valor_final,
                tipo_repasse='fixo',
                observacao=f"Repasse semanal automático ({data_inicio} a {data_fim})"
            )
            resultado.append(f"{motoboy.nome} — R$ {valor_final:.2f}")

    return resultado
