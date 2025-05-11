from django.core.management.base import BaseCommand
from motopro.models import Contrato_Item


class Command(BaseCommand):
    help = 'Popula itens padrão de contrato para motoboys'

    def handle(self, *args, **kwargs):
        itens_contrato = [
            {
                "nome": "Valor por entrega",
                "chave_sistema": "motoboy_valor_entrega",
                "tipo_dado": "float",
                "valor_padrao": "5.00",
                "obrigatorio": True,
            },
            {
                "nome": "Bônus por pontualidade",
                "chave_sistema": "motoboy_bonus_pontualidade",
                "tipo_dado": "float",
                "valor_padrao": "0.00",
                "obrigatorio": False,
            },
            {
                "nome": "Aceita turnos noturnos",
                "chave_sistema": "motoboy_aceita_turno_noturno",
                "tipo_dado": "boolean",
                "valor_padrao": "False",
                "obrigatorio": False,
            },
            {
                "nome": "Número máximo de entregas por dia",
                "chave_sistema": "motoboy_max_entregas_dia",
                "tipo_dado": "integer",
                "valor_padrao": "30",
                "obrigatorio": True,
            },
             {
                "nome": "Número mínimo de entregas por dia",
                "chave_sistema": "motoboy_min_entregas_dia",
                "tipo_dado": "integer",
                "valor_padrao": "5",
                "obrigatorio": True,
            },
            {
                "nome": "Tempo mínimo entre entregas (min)",
                "chave_sistema": "motoboy_tempo_minimo_entre_entregas",
                "tipo_dado": "integer",
                "valor_padrao": "5",
                "obrigatorio": False,
            },
            {
                "nome": "Permite adiantamento de valor",
                "chave_sistema": "motoboy_permite_adiantamento",
                "tipo_dado": "boolean",
                "valor_padrao": "False",
                "obrigatorio": False,
            },
            {
                "nome": "Reembolso por km extra",
                "chave_sistema": "motoboy_reembolso_km_extra",
                "tipo_dado": "float",
                "valor_padrao": "0.50",
                "obrigatorio": False,
            },
            {
                "nome": "Valor mínimo por turno",
                "chave_sistema": "motoboy_valor_minimo_turno",
                "tipo_dado": "float",
                "valor_padrao": "50.00",
                "obrigatorio": True,
            },
            {
                "nome": "Aceita entregas com pagamento em dinheiro",
                "chave_sistema": "motoboy_aceita_dinheiro",
                "tipo_dado": "boolean",
                "valor_padrao": "True",
                "obrigatorio": False,
            },
            {
                "nome": "Frequência mínima semanal (dias)",
                "chave_sistema": "motoboy_frequencia_semanal_minima",
                "tipo_dado": "integer",
                "valor_padrao": "3",
                "obrigatorio": False,
            },
        ]

        for item in itens_contrato:
            obj, created = Contrato_Item.objects.get_or_create(
                chave_sistema=item["chave_sistema"],
                defaults=item
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✔ Criado: {item["nome"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'ℹ Já existe: {item["nome"]}'))
