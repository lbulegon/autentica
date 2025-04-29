from rest_framework import serializers
from motopro.models import Vaga
from motopro.models import Estabelecimento

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'

class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        fields = '__all__'
