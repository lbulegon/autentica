from rest_framework import serializers
from motopro.models import Vaga

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'
