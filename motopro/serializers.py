
# serializers.py

from rest_framework import serializers
from .models import TarefaConfig

class TarefaConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarefaConfig
        fields = ['id', 'nome', 'horario', 'ativa']
