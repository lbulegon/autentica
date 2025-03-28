from rest_framework import serializers
from motopro.models import vaga
from motopro.models import estabelecimento

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = vaga
        fields = '__all__'

class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = estabelecimento
        fields = '__all__'
