from django import forms
from motopro.models import vaga
class VagaForm(forms.ModelForm):
    class Meta:
        model = vaga
        fields = ['estabelecimento', 'observacoes', 'valor', 'status', 'motoboy']
