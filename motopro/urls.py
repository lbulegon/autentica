from django.urls import path, include
from .views import View_gerar_repasses_semanais
from . import views

from rest_framework.routers import DefaultRouter
from .views import TarefaConfigViewSet

from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'tarefas', TarefaConfigViewSet)

urlpatterns = [
    path('admin/gerar-repasses/', View_gerar_repasses_semanais, name='gerar-repasses-semanais'),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('atribuir-pedido/', views.atribuir_pedido_a_motoboy, name='atribuir_pedido'),
    path('rota/', views.visualizar_rota, name='visualizar_rota'),
    path('rota/<int:pedido_id>/', views.visualizar_rota, name='visualizar_rota_pedido'),
    path('webhook/ifood/', views.ifood_webhook, name='ifood_webhook'),
]







