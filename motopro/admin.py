from django.contrib import admin, messages 
from django.contrib.admin import DateFieldListFilter
from .models import Estabelecimento, Supervisor_Estabelecimento,Supervisor_Motoboy # ou o caminho correto se estiver em outro lugar
from .models import  Vaga, Supervisor, Estabelecimento_Contrato, Estabelecimento_Contrato_Item
from .models import Motoboy, Motoboy_Repasse, Motoboy_Alocacao, Motoboy_Ranking 
from .models import Configuracao, Contrato_Item, Motoboy_BandaVaga
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.html import format_html
from django.urls import path, reverse
from datetime import date, datetime
from .utils import calcular_repasse_diario
from .forms import RepasseManualForm  # você deve criar esse forms.py
from django.db.models import Sum


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
admin.site.register(Motoboy_BandaVaga) 

@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'nivel', 'acoes_personalizadas')
    search_fields = ('nome', 'apelido')  
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:motoboy_id>/gerar-repasse/', self.admin_site.admin_view(self.gerar_repasse_view), name='motoboy-gerar-repasse'),
            path('<int:motoboy_id>/ver-repasses/', self.admin_site.admin_view(self.ver_repasses_view), name='motoboy-ver-repasses'),
        ]
        return custom_urls + urls

    def acoes_personalizadas(self, obj):
        gerar_url = reverse('admin:motoboy-gerar-repasse', args=[obj.id])
        ver_url = reverse('admin:motoboy-ver-repasses', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Gerar Repasse</a>&nbsp;'
            '<a class="button" href="{}">Ver Repasses</a>',
            gerar_url, ver_url
        )

    def gerar_repasse_view(self, request, motoboy_id):
        motoboy = Motoboy.objects.get(pk=motoboy_id)

        if request.method == 'POST':
            form = RepasseManualForm(request.POST)
            if form.is_valid():
                Motoboy_Repasse.objects.create(
                    motoboy=motoboy,
                    data_referencia=form.cleaned_data['data_referencia'],
                    valor=form.cleaned_data['valor'],
                    tipo_repasse=form.cleaned_data['tipo_repasse'],
                    observacao=form.cleaned_data['observacao'],
                )
                messages.success(request, f"Repasse registrado com sucesso.")
                return redirect(reverse('admin:motopro_motoboy_changelist'))
        else:
            form = RepasseManualForm()

        return render(request, 'admin/motoboy_gerar_repasse.html', {
            'form': form,
            'motoboy': motoboy,
        })

    def ver_repasses_view(self, request, motoboy_id):
        motoboy = Motoboy.objects.get(pk=motoboy_id)

        inicio_str = request.GET.get('inicio')
        fim_str = request.GET.get('fim')

        repasses = Motoboy_Repasse.objects.filter(motoboy=motoboy)

        if inicio_str:
            try:
                data_inicio = datetime.strptime(inicio_str, '%Y-%m-%d').date()
                repasses = repasses.filter(data_referencia__gte=data_inicio)
            except ValueError:
                messages.warning(request, "Data de início inválida")

        if fim_str:
            try:
                data_fim = datetime.strptime(fim_str, '%Y-%m-%d').date()
                repasses = repasses.filter(data_referencia__lte=data_fim)
            except ValueError:
              messages.warning(request, "Data de fim inválida")

        repasses = repasses.order_by('-data_referencia')
        total = repasses.aggregate(total=Sum('valor'))['total'] or 0

        return render(request, 'admin/motoboy_lista_repasses.html', {
            'motoboy': motoboy,
            'repasses': repasses,
            'total': total,
            'inicio': inicio_str or '',
            'fim': fim_str or '',
    })


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
