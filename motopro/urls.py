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
    path('webhook/ifood/', views.webhook_ifood, name='webhook_ifood'),
    path('api/', include(router.urls)),
     path('api-token-auth/', obtain_auth_token),

]







