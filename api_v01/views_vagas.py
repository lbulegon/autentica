from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from motopro.models import vaga
from .serializers import VagaSerializer

class VagaViewSet(viewsets.ModelViewSet):
    queryset = vaga.objects.all()
    serializer_class = VagaSerializer
    permission_classes = [IsAuthenticated]  # Exige login para acessar
