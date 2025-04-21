from django.contrib import admin
from .models import estabelecimento, supervisorestabelecimento,supervisormotoboy # ou o caminho correto se estiver em outro lugar
from .models import motoboy, vaga, supervisor, estabelecimentocontrato,  alocacaomotoboy

admin.site.register(estabelecimento)
admin.site.register(estabelecimentocontrato)
admin.site.register(supervisor)
admin.site.register(supervisorestabelecimento)
admin.site.register(supervisormotoboy)
admin.site.register(motoboy)
admin.site.register(alocacaomotoboy)

class VagaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "motoboy":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                try:
                    vvaga = vaga.objects.get(pk=object_id)
                    estabelecimento = vvaga.contrato.estabelecimento

                    # Supervisor responsável
                    supervisor_rel = supervisorestabelecimento.objects.filter(estabelecimento=estabelecimento).first()
                    if supervisor_rel:
                        supervisor = supervisor_rel.supervisor

                        # Motoboys vinculados ao supervisor
                        motoboy_ids = supervisormotoboy.objects.filter(supervisor=supervisor).values_list('motoboy_id', flat=True)

                        # Data e turno da vaga
                        data_vaga = vvaga.data_da_vaga.date() if vvaga.data_da_vaga else None
                        turno = vvaga.contrato

                        # Motoboys já alocados para este turno e data
                        motoboys_alocados = alocacaomotoboy.objects.filter(
                            turno=turno,
                            vaga__data_da_vaga__date=data_vaga,
                            status='alocado'
                        ).values_list('motoboy_id', flat=True)

                        # Motoboys que podem ser escolhidos
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

        # Cria ou atualiza a alocação
        if obj.motoboy and obj.contrato:
            alocacaomotoboy.objects.update_or_create(
                motoboy=obj.motoboy,
                vaga=obj,
                turno=obj.contrato,
                defaults={'status': 'alocado'}
            )

admin.site.register(vaga, VagaAdmin)
