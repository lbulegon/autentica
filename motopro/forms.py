from django import forms
from motopro.models import vaga
from motopro.models import estabeleciomento
class VagaForm(forms.ModelForm):
    class Meta:
        model = vaga
        fields = ['estabelecimento', 'observacoes', 'valor', 'status', 'motoboy']

class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = estabeleciomento
        fields = '__all__'