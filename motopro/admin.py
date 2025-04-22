from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
class AlocacaoMotoboyAdmin(admin.ModelAdmin):
    fields = ['vaga', 'motoboy', 'status']  # Exibe só o que você quer

    def save_model(self, request, obj, form, change):
        # Preenche o campo 'turno' automaticamente a partir da vaga
        if obj.vaga and obj.vaga.contrato:
            obj.turno = obj.vaga.contrato
        super().save_model(request, obj, form, change)

admin.site.register(alocacaomotoboy,AlocacaoMotoboyAdmin)



# Filtro por Estabelecimento via contrato.estabelecimento
class EstabelecimentoFilter(admin.SimpleListFilter):
    title = _('Estabelecimento')
    parameter_name = 'estabelecimento'

    def lookups(self, request, model_admin):
        estabelecimentos = set(
            v.contrato.estabelecimento for v in vaga.objects.select_related('contrato__estabelecimento')
            if v.contrato and v.contrato.estabelecimento
        )
        return [(e.id, e.nome) for e in estabelecimentos]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contrato__estabelecimento__id=self.value())
        return queryset


@admin.register(vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = [
        "id", "data_da_vaga", "turno", "get_estabelecimento",
        "get_motoboy_alocado", "status"
    ]
    list_filter = ["status", "data_da_vaga", "turno", EstabelecimentoFilter]
    search_fields = ["id", "contrato__estabelecimento__nome"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "motoboy":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                try:
                    vvaga = vaga.objects.get(pk=object_id)
                    estabelecimento = vvaga.contrato.estabelecimento

                    supervisor_rel = supervisorestabelecimento.objects.filter(
                        estabelecimento=estabelecimento).first()
                    if supervisor_rel:
                        supervisor = supervisor_rel.supervisor

                        motoboy_ids = supervisormotoboy.objects.filter(
                            supervisor=supervisor
                        ).values_list('motoboy_id', flat=True)

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Atualiza a alocação e o status da vaga
        if obj.motoboy:
            alocacaomotoboy.objects.update_or_create(
                motoboy=obj.motoboy,
                vaga=obj,
                turno=obj.contrato,
                defaults={'status': 'alocado'}
            )
            obj.status = 'preenchida'
            obj.save(update_fields=["status"])
        else:
            obj.status = 'aberta'
            obj.save(update_fields=["status"])
            alocacaomotoboy.objects.filter(vaga=obj).delete()

    def get_estabelecimento(self, obj):
        return obj.contrato.estabelecimento.nome if obj.contrato and obj.contrato.estabelecimento else "-"
    get_estabelecimento.short_description = "Estabelecimento"

    def get_motoboy_alocado(self, obj):
        alocacao = alocacaomotoboy.objects.filter(
            vaga=obj, status='alocado'
        ).select_related('motoboy').first()
        return alocacao.motoboy.nome if alocacao else "-"
    get_motoboy_alocado.short_description = "Motoboy Alocado"
