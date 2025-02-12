from django import forms
from motopro.models import vaga

class VagaForm(forms.ModelForm):
    class Meta:
        model = vaga
        fields = ['empresa_id', 'observacoes', 'valor', 'status', 'motoboy_id']