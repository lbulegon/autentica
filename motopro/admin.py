from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import estabelecimento, supervisorestabelecimento,supervisormotoboy # ou o caminho correto se estiver em outro lugar
from .models import motoboy, vaga, supervisor, estabelecimentocontrato,  alocacaomotoboy

admin.site.register(estabelecimento)
admin.site.register(estabelecimentocontrato)
admin.site.register(supervisor)
admin.site.register(supervisorestabelecimento)
admin.site.register(supervisormotoboy)
@admin.register(motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    search_fields = ["nome", "cpf", "telefone"]  # Campo de busca no topo
    list_display = ["nome", "cpf", "telefone",  "status"]  # Colunas visíveis na listagem
    list_filter = [ "status"]  # Filtros laterais
    ordering = ["nome"]  # Ordenação padrão
#admin.site.register(alocacaomotoboy)

#@admin.register(alocacaomotoboy)
from django.contrib import admin
from motopro.models import alocacaomotoboy, motoboy

class AlocacaoMotoboyAdmin(admin.ModelAdmin):
    fields = ['vaga', 'motoboy', 'entregas_realizadas', 'status']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "motoboy":
            user = request.user
            # Aqui assumimos que o supervisor está relacionado a estabelecimentos
            kwargs["queryset"] = motoboy.objects.filter(
                estabelecimento__supervisor=user
            ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.vaga and obj.vaga.contrato:
            obj.turno = obj.vaga.contrato
        super().save_model(request, obj, form, change)

admin.site.register(alocacaomotoboy, AlocacaoMotoboyAdmin)


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
                    vvaga = vaga.objects.get(pk=object_id)
                    estabelecimento = vvaga.contrato.estabelecimento

                    supervisor_rel = supervisorestabelecimento.objects.filter(estabelecimento=estabelecimento).first()
                    if supervisor_rel:
                        supervisor = supervisor_rel.supervisor

                        motoboy_ids = supervisormotoboy.objects.filter(
                            supervisor=supervisor).values_list('motoboy_id', flat=True)

                        data_vaga = vvaga.data_da_vaga.date() if vvaga.data_da_vaga else None
                        turno = vvaga.contrato

                        motoboys_alocados = alocacaomotoboy.objects.filter(
                            turno=turno,
                            vaga__data_da_vaga__date=data_vaga,
                            status='alocado'
                        ).values_list('motoboy_id', flat=True)

                        kwargs["queryset"] = motoboy.objects.filter(
                            id__in=motoboy_ids
                        ).exclude(
                            id__in=motoboys_alocados
                        )

                except vaga.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(vaga, VagaAdmin)
