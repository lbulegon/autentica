from rest_framework import serializers
from motopro.models import vaga

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = vaga
        fields = '__all__'
