from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum
from motopro.models import vaga, estabelecimentofatura, estabelecimento

class Command(BaseCommand):
    help = 'Gera faturas mensais por estabelecimento com base nas vagas utilizadas'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        primeiro_dia_mes = hoje.replace(day=1)

        estabelecimentos = estabelecimento.objects.all()

        for est in estabelecimentos:
            vagas_do_mes = vaga.objects.filter(
                contrato__estabelecimento=est,
                data_da_vaga__gte=primeiro_dia_mes,
                data_da_vaga__lte=hoje,
                status="preenchida"  # Adicionado filtro para vagas com status "preenchida"
            )

            quantidade_vagas = vagas_do_mes.count()
            valor_total = vagas_do_mes.aggregate(total=Sum('contrato__valor_atribuido'))['total'] or 0

            if quantidade_vagas == 0:
                self.stdout.write(f"Sem vagas para faturar em {est.nome}")
                continue

            fatura, criada = estabelecimentofatura.objects.get_or_create(
                estabelecimento=est,
                data_referencia=primeiro_dia_mes,
                defaults={
                    'valor_total': valor_total,
                    'status': 'aberta',
                    'quantidade_alocacoes': quantidade_vagas
                }
            )

            if not criada:
                fatura.valor_total = valor_total
                fatura.quantidade_alocacoes = quantidade_vagas
                fatura.save()

            self.stdout.write(
                f"Fatura {'criada' if criada else 'atualizada'}: {est.nome} | R$ {valor_total:.2f} | {quantidade_vagas} alocações"
            )
