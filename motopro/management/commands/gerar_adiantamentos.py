from django.db.models import Sum
from decimal import Decimal
from motopro.models import Motoboy, Vaga, Motoboy_Desconto, Motoboy_Adiantamento, Motoboy_Ranking

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

    # Valor final doi adiantamento
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
