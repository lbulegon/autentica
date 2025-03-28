from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from motopro.models import estabelecimento
from .serializers import EstabelecimentoSerializer

class EstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = estabelecimento.objects.all()
    serializer_class = EstabelecimentoSerializer
    #permission_classes = [IsAuthenticated]  # Exige login para acessar
