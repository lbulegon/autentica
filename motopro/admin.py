
from .models import Estabelecimento, Supervisor_Estabelecimento,Supervisor_Motoboy # ou o caminho correto se estiver em outro lugar
from .models import  Vaga, Supervisor, Estabelecimento_Contrato, Estabelecimento_Contrato_Item
from .models import Motoboy, Motoboy_Adiantamento, Motoboy_Alocacao, Motoboy_Ranking 
from .models import Configuracao, Contrato_Item, Motoboy_BandaVaga, Motoboy_Contrato, Motoboy_Contrato_Item
from .models import TarefaConfig
from .utils  import calcular_adiantamento_diario
from .forms  import AdiantamentoManualForm  # você deve criar esse forms.py

from django.shortcuts import redirect, get_object_or_404, render,redirect
from django.utils.html import format_html
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.contrib import admin, messages 
from django.contrib.admin import DateFieldListFilter

from datetime import date, datetime,timedelta
from decimal import Decimal


admin.site.register(Contrato_Item) 
admin.site.register(Configuracao)
admin.site.register(Estabelecimento)
admin.site.register(Estabelecimento_Contrato)
admin.site.register(Estabelecimento_Contrato_Item)
admin.site.register(Supervisor)
admin.site.register(Supervisor_Estabelecimento)
admin.site.register(Supervisor_Motoboy)
admin.site.register(Motoboy_Ranking)
admin.site.register(Motoboy_Adiantamento)
admin.site.register(Motoboy_BandaVaga) 
admin.site.register(Motoboy_Contrato)
admin.site.register(Motoboy_Contrato_Item)  



@admin.register(TarefaConfig)
class TarefaConfigAdmin(admin.ModelAdmin):
    list_display = ('nome', 'horario', 'ativa')
    list_editable = ('ativa', 'horario')


@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'nivel', 'acoes_personalizadas', 'link_repasse')

    search_fields = ('nome', 'apelido')  

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:motoboy_id>/gerar-adiantamento/', self.admin_site.admin_view(self.gerar_adiantamento_view), name='motoboy-gerar-adiantamento'),
            path('<int:motoboy_id>/ver-adiantamentos/', self.admin_site.admin_view(self.ver_adiantamentos_view), name='motoboy-ver-adiantamentos'),
        ]
        return custom_urls + urls

    def acoes_personalizadas(self, obj):
        gerar_url = reverse('admin:motoboy-gerar-adiantamento', args=[obj.id])
        ver_url = reverse('admin:motoboy-ver-adiantamentos', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Gerar Adiantamento</a>&nbsp;'
            '<a class="button" href="{}">Ver Adiantamentos</a>',
            gerar_url, ver_url
        )

    def gerar_adiantamento_view(self, request, motoboy_id):
        motoboy = Motoboy.objects.get(pk=motoboy_id)

        if request.method == 'POST':
            form = AdiantamentoManualForm(request.POST)
            if form.is_valid():
                Motoboy_Adiantamento.objects.create(
                    motoboy=motoboy,
                    data_referencia=form.cleaned_data['data_referencia'],
                    valor=form.cleaned_data['valor'],
                    tipo_adiantamento=form.cleaned_data['tipo_adiantamento'],
                    observacao=form.cleaned_data['observacao'],
                )
                messages.success(request, f"Adiantamento registrado com sucesso.")
                return redirect(reverse('admin:motopro_motoboy_changelist'))
        else:
            form = AdiantamentoManualForm()

        return render(request, 'admin/motoboy_gerar_adiantamento.html', {
            'form': form,
            'motoboy': motoboy,
        })
    

    def link_repasse(self, obj):
        url = reverse('gerar-repasses-semanais')
        return format_html('<a class="button" href="{}">Repasse Semanal</a>', url)

    link_repasse.short_description = 'Repasse'

    def ver_adiantamentos_view(self, request, motoboy_id):
        motoboy = Motoboy.objects.get(pk=motoboy_id)

        inicio_str = request.GET.get('inicio')
        fim_str = request.GET.get('fim')

        adiantamentos = Motoboy_Adiantamento.objects.filter(motoboy=motoboy)

        if inicio_str:
            try:
                data_inicio = datetime.strptime(inicio_str, '%Y-%m-%d').date()
                adiantamentos = adiantamentos.filter(data_referencia__gte=data_inicio)
            except ValueError:
                messages.warning(request, "Data de início inválida")

        if fim_str:
            try:
                data_fim = datetime.strptime(fim_str, '%Y-%m-%d').date()
                adiantamentos = adiantamentos.filter(data_referencia__lte=data_fim)
            except ValueError:
              messages.warning(request, "Data de fim inválida")

        adiantamentos = adiantamentos.order_by('-data_referencia')
        total = adiantamentos.aggregate(total=Sum('valor'))['total'] or 0

        return render(request, 'admin/motoboy_lista_adiantamentos.html', {
            'motoboy': motoboy,
            'adiantamentos': adiantamentos,
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


class RelatorioAdminView(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gerar-repasses-semanais/', self.admin_site.admin_view(self.executar_repasses), name='executar-repasses-semanais'),
        ]
        return custom_urls + urls

    def executar_repasses(self, request):
        hoje = date.today()
        semana_passada = hoje - timedelta(days=6)

        resultado = gerar_repasses_semanais(data_inicio=semana_passada, data_fim=hoje)

        if resultado:
            html_lista = "<ul>" + "".join([f"<li>{r}</li>" for r in resultado]) + "</ul>"
            messages.success(request, mark_safe(f"Repasses gerados:<br>{html_lista}"))
        else:
            messages.warning(request, "Nenhum repasse pendente para a semana.")

        return redirect(reverse('admin:motopro_motoboy_changelist'))
