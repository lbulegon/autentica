from django.contrib import admin
from .models import estabelecimento, supervisorestabelecimento,supervisormotoboy # ou o caminho correto se estiver em outro lugar
from .models import motoboy, vaga, supervisor, estabelecimentocontrato


admin.site.register(estabelecimento)
admin.site.register(estabelecimentocontrato)
admin.site.register(supervisor)
admin.site.register(supervisorestabelecimento)
admin.site.register(supervisormotoboy)
admin.site.register(motoboy)


class VagaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "motoboy":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                vvaga = vaga.objects.get(pk=object_id)
                estabelecimento = vvaga.contrato.estabelecimento

                supervisor_rel = supervisorestabelecimento.objects.filter(estabelecimento=estabelecimento).first()
                if supervisor_rel:
                    supervisor = supervisor_rel.supervisor
                    motoboy_ids = supervisormotoboy.objects.filter(supervisor=supervisor).values_list('motoboy_id', flat=True)
                    kwargs["queryset"] = motoboy.objects.filter(id__in=motoboy_ids)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(vaga, VagaAdmin)