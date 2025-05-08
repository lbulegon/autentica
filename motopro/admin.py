from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Estabelecimento, Supervisor_Estabelecimento,Supervisor_Motoboy # ou o caminho correto se estiver em outro lugar
from .models import Motoboy, Vaga, Supervisor, Estabelecimento_Contrato, Estabelecimento_Contrato_Item, Motoboy_Alocacao,Motoboy_Ranking
#from .models import Slot, Slot_Candidatura, Slot_Vaga
from .models import Configuracao,  Contrato_Item 
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.urls import path

admin.site.register(Motoboy_Ranking)
admin.site.register(Motoboy)
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
    search_fields   = ["nome", "cpf", "telefone"]  # Campo de busca no topo
    list_display    = ["nome", "cpf", "telefone",  "status"]  # Colunas visíveis na listagem
    list_filter     = [ "status"]  # Filtros laterais
    ordering        = ["nome"]  # Ordenação padrão
#admin.site.register(alocacaomotoboy)

#@admin.register(alocacaomotoboy)

class MotoboyAlocacaoAdmin(admin.ModelAdmin):
    list_display = ('vaga', 'motoboy', 'entregas_realizadas', 'desalocar_botao')
    list_filter = ('vaga__status', 'motoboy')
    search_fields = ('vaga__id', 'motoboy__nome')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['vaga'].queryset = Vaga.objects.filter(status='aberta')
        else:
            form.base_fields['vaga'].queryset = Vaga.objects.filter(pk=obj.vaga.pk)
            form.base_fields['vaga'].disabled = True
        return form

    def desalocar_botao(self, obj):
        return format_html(
            '<a class="button" href="{}">Desalocar</a>',
            f'../desalocar/{obj.id}/'
        )
    desalocar_botao.short_description = 'Ações'
    desalocar_botao.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('desalocar/<int:alocacao_id>/', self.admin_site.admin_view(self.desalocar_view), name='desalocar_motoboy'),
        ]
        return custom_urls + urls

    def desalocar_view(self, request, alocacao_id):
        alocacao = get_object_or_404(Motoboy_Alocacao, pk=alocacao_id)
        vaga = alocacao.vaga

        # Remove a alocação
        alocacao.delete()

        # Atualiza status da vaga para aberta
        vaga.status = 'aberta'
        vaga.save()

        self.message_user(request, f"Motoboy desalocado da vaga {vaga.id} com sucesso!", level=messages.SUCCESS)
        return redirect(f'/admin/app_nome/motoboy_alocacao/')  # troque `app_nome` pelo nome real da sua app

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
