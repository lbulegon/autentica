from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_vagas import VagaViewSet

router = DefaultRouter()
router.register(r'vagas', VagaViewSet, basename='vaga')

urlpatterns = [
    path('', include(router.urls)),
]
