# motopro/utils.py
from decimal import Decimal
from motopro.models import Vaga, Motoboy_Alocacao

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
