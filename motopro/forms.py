from django import forms
from motopro.models import Vaga
from motopro.models import Estabelecimento
from motopro.models import Motoboy, Motoboy_Repasse
from motopro.models import Supervisor
from django.contrib.auth.forms import AuthenticationForm
import datetime
from decimal import Decimal
class RepasseManualForm(forms.Form):
    data_referencia = forms.DateField(
        label="Data do Repasse",
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )

    valor = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal('0.01'),
        label="Valor a Repassar (R$)"
    )

    tipo_repasse = forms.ChoiceField(
        choices=Motoboy_Repasse.TIPO_REPASSE_CHOICES,
        label="Tipo de Repasse"
    )

    observacao = forms.CharField(
        required=False, widget=forms.Textarea, label="Observação (opcional)"
    )







class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [ 'observacao','data_da_vaga',  'status']

class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = Estabelecimento
        fields = '__all__'
class MotoboyForm(forms.ModelForm):
    class Meta:
        model = Motoboy
        fields = '__all__'        

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = '__all__'                
       
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
