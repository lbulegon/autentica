from django import forms
from motopro.models import vaga
from motopro.models import estabelecimento
from motopro.models import motoboy
from motopro.models import supervisor

class VagaForm(forms.ModelForm):
    class Meta:
        model = vaga
        fields = ['estabelecimento', 'observacoes', 'valor', 'status', 'motoboy']

class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = estabelecimento
        fields = '__all__'


class MotoboyForm(forms.ModelForm):
    class Meta:
        model = motoboy
        fields = '__all__'        



class SupervisorForm(forms.ModelForm):
    class Meta:
        model = supervisor
        fields = '__all__'                