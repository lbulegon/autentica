# motopro/utils.py
from decimal import Decimal
from django.db.models import Sum
from decimal import Decimal
from motopro.models import Motoboy, Vaga, Motoboy_Desconto, Motoboy_Adiantamento, Motoboy_Ranking, Motoboy_Alocacao

def calcular_pagamento(estabelecimento, motoboy, data_inicio, data_fim):
    vagas = Vaga.objects.filter(
        contrato__estabelecimento=estabelecimento,
        data_da_vaga__range=(data_inicio, data_fim),
        status='finalizada'
    )

    alocacoes = Motoboy_Alocacao.objects.filter(
        motoboy=motoboy,
        vaga__in=vagas
    )

    valor_por_vaga = Decimal('100.00')
    total = valor_por_vaga * alocacoes.count()

    return {
        'motoboy': motoboy.nome_completo,
        'estabelecimento': estabelecimento.nome,
        'quantidade_vagas': alocacoes.count(),
        'total_motoboy_recebe': round(total, 2)
    }


def calcular_adiantamento_diario(motoboy, data):
    # Buscar as vagas alocadas no dia
    alocacoes = motoboy.motoboy_alocacao_set.filter(vaga__data_da_vaga=data)
    total_entregas = alocacoes.aggregate(total=Sum('entregas_realizadas'))['total'] or 0

    # Buscar o bônus por entrega do ranking (caso exista)
    ranking = Motoboy_Ranking.objects.filter(motoboy=motoboy).first()
    bonus_por_entrega = ranking.bonus_por_entrega if ranking else Decimal('6.00')

    # Calcular valor bruto
    valor_bruto = Decimal(total_entregas) * bonus_por_entrega

    # Buscar descontos no dia
    descontos = Motoboy_Desconto.objects.filter(motoboy=motoboy, data=data, ativo=True)
    total_descontos = descontos.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

    # Valor final a adiantamento
    valor_final = valor_bruto - total_descontos

    # Criar registro de adiantamento
    adiantamento = Motoboy_Adiantamento.objects.create(
        motoboy=motoboy,
        data_referencia=data,
        valor=valor_final,
        tipo_adiantamento='fixo',
        observacao=f"Entregas: {total_entregas}, Bônus: R$ {bonus_por_entrega}, Descontos: R$ {total_descontos}"
    )

    return adiantamento

def calcular_adiantamento_por_bandas(alocacao):
    contrato = alocacao.vaga.contrato
    total = Decimal('0.00')

    for banda in alocacao.bandas.all():
        chave_valor = f'faixa_km_{banda.faixa_km}'
        valor_unitario = contrato.get_valor_item(chave_valor) or Decimal('0.00')
        total += valor_unitario * banda.quantidade

    return total
