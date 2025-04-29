from django import forms
from motopro.models import Vaga
from motopro.models import Estabelecimento
from motopro.models import Motoboy
from motopro.models import Supervisor
from django.contrib.auth.forms import AuthenticationForm

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
