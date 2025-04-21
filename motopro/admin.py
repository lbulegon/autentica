from django.contrib import admin
from .models import estabelecimento, supervisorestabelecimento,supervisormotoboy # ou o caminho correto se estiver em outro lugar
from .models import motoboy, vaga, supervisor, estabelecimentocontrato
from .models import  supervisorestabelecimento, supervisormotoboy

admin.site.register(estabelecimento)
admin.site.register(estabelecimentocontrato)
admin.site.register(motoboy)
admin.site.register(supervisor)
admin.site.register(supervisorestabelecimento)
admin.site.register(supervisormotoboy)
admin.site.register(estabelecimentocontrato)
admin.site.register(vaga)

