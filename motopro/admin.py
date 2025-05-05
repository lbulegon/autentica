from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Estabelecimento, Supervisor_Estabelecimento,Supervisor_Motoboy # ou o caminho correto se estiver em outro lugar
from .models import Motoboy, Vaga, Supervisor, Estabelecimento_Contrato, Estabelecimento_Contrato_Item, Motoboy_Alocacao,Motoboy_Ranking
#from .models import Slot, Slot_Candidatura, Slot_Vaga
from .models import Configuracao,  Contrato_Item 


admin.site.register(Motoboy_Ranking)
admin.site.register(Contrato_Item) 
admin.site.register(Configuracao)
# admin.site.register(Slot)
# admin.site.register(Slot_Candidatura)
# admin.site.register(Slot_Vaga)
admin.site.register(Estabelecimento)
admin.site.register(Estabelecimento_Contrato)
admin.site.register(Estabelecimento_Contrato_Item)
admin.site.register(Supervisor)
admin.site.register(Supervisor_Estabelecimento)
admin.site.register(Supervisor_Motoboy)
#@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    search_fields = ["nome", "cpf", "telefone"]  # Campo de busca no topo
    list_display = ["nome", "cpf", "telefone",  "status"]  # Colunas visíveis na listagem
    list_filter = [ "status"]  # Filtros laterais
    ordering = ["nome"]  # Ordenação padrão
#admin.site.register(alocacaomotoboy)

#@admin.register(alocacaomotoboy)
class AlocacaoMotoboyAdmin(admin.ModelAdmin):
    fields = ['vaga', 'motoboy', 'entregas_realizadas' ,'status']  # Exibe só o que você quer

    def save_model(self, request, obj, form, change):
        # Preenche o campo 'turno' automaticamente a partir da vaga
        if obj.vaga and obj.vaga.contrato:
            obj.turno = obj.vaga.contrato
        super().save_model(request, obj, form, change)

admin.site.register(Motoboy_Alocacao,AlocacaoMotoboyAdmin)

class VagaAdmin(admin.ModelAdmin):
    list_filter = [
        'status',
        ('data_da_vaga', DateFieldListFilter),
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "motoboy":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                try:
                    vvaga = Vaga.objects.get(pk=object_id)
                    estabelecimento = vvaga.contrato.estabelecimento

                    supervisor_rel = Supervisor_Estabelecimento.objects.filter(estabelecimento=estabelecimento).first()
                    if supervisor_rel:
                        supervisor = supervisor_rel.supervisor

                        motoboy_ids = Supervisor_Motoboy.objects.filter(
                            supervisor=supervisor).values_list('motoboy_id', flat=True)

                        data_vaga = vvaga.data_da_vaga.date() if vvaga.data_da_vaga else None
                        turno = vvaga.contrato

                        motoboys_alocados = Motoboy_Alocacao.objects.filter(
                            turno=turno,
                            vaga__data_da_vaga__date=data_vaga,
                            status='alocado'
                        ).values_list('motoboy_id', flat=True)

                        kwargs["queryset"] = Motoboy.objects.filter(
                            id__in=motoboy_ids
                        ).exclude(
                            id__in=motoboys_alocados
                        )

                except vaga.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Vaga, VagaAdmin)
