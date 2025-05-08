from django.contrib import admin, messages 
from django.contrib.admin import DateFieldListFilter
from .models import Estabelecimento, Supervisor_Estabelecimento,Supervisor_Motoboy # ou o caminho correto se estiver em outro lugar
from .models import  Vaga, Supervisor, Estabelecimento_Contrato, Estabelecimento_Contrato_Item
from .models import Motoboy, Motoboy_Repasse, Motoboy_Alocacao, Motoboy_Ranking 
from .models import Configuracao, Contrato_Item
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.urls import path, reverse
from datetime import date
from .utils import calcular_repasse_diario



admin.site.register(Contrato_Item) 
admin.site.register(Configuracao)
admin.site.register(Estabelecimento)
admin.site.register(Estabelecimento_Contrato)
admin.site.register(Estabelecimento_Contrato_Item)
admin.site.register(Supervisor)
admin.site.register(Supervisor_Estabelecimento)
admin.site.register(Supervisor_Motoboy)

admin.site.register(Motoboy_Ranking)
admin.site.register(Motoboy_Repasse)
@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'nivel', 'gerar_repasse_link')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:motoboy_id>/gerar-repasse/', self.admin_site.admin_view(self.gerar_repasse_view), name='gerar-repasse'),
        ]
        return custom_urls + urls

    def gerar_repasse_link(self, obj):
        return format_html('<a class="button" href="{}">Gerar Repasse de Hoje</a>', f'{obj.id}/gerar-repasse/')
    gerar_repasse_link.short_description = 'Repasse'
    gerar_repasse_link.allow_tags = True

    def gerar_repasse_view(self, request, motoboy_id):
        motoboy = Motoboy.objects.get(pk=motoboy_id)
        hoje = date.today()
        repasse = calcular_repasse_diario(motoboy, hoje)
        messages.success(request, f"Repasse gerado: R$ {repasse.valor:.2f} em {repasse.data_referencia}")
        change_url = reverse('admin:motopro_motoboy_change', args=[motoboy_id])
        return redirect(change_url)
    
admin.site.register(Motoboy_Alocacao)




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
