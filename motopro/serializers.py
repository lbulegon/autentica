
# serializers.py

from rest_framework import serializers
from .models import TarefaConfig
from .models import IfoodWebhookEvent
class TarefaConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarefaConfig
        fields = ['id', 'nome', 'horario', 'ativa']

class IfoodWebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = IfoodWebhookEvent
        fields = '__all__'

