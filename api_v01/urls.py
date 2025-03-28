from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_vagas import VagaViewSet

router = DefaultRouter()
router.register(r'vagas', VagaViewSet, basename='vaga')
router.register(r'estabelecimentos', EstabelecimentoViewSet, basename='estabelecimento')

urlpatterns = [
    path('', include(router.urls)),
]
