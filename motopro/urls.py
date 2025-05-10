from django.urls import path
from .views import View_gerar_repasses_semanais

urlpatterns = [
    path('admin/gerar-repasses/', View_gerar_repasses_semanais, name='gerar-repasses-semanais'),
]
