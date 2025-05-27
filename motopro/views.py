import json
from decimal import Decimal
import hmac
import hashlib
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy

from motopro.models import Vaga, Estabelecimento, Motoboy, Supervisor, Estabelecimento_Contrato

from motopro.forms import VagaForm, EstabelecimentoForm, MotoboyForm, Motoboy_Adiantamento, SupervisorForm, LoginForm


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TarefaConfig
from .serializers import TarefaConfigSerializer
# views.py

from django.http import JsonResponse
from motopro.services.pedido import atribuir_pedido_a_motoboy, atualizar_status_pedido
from motopro.services.roteirizacao import calcular_rota_google

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import IfoodWebhookEvent, Motoboy
from motopro.serializers import IfoodWebhookEventSerializer





IFOOD_SECRET = 'SUA_CHAVE_SECRETA_DO_IFOOD'


class TarefaConfigViewSet(viewsets.ModelViewSet):
    queryset = TarefaConfig.objects.all()
    serializer_class = TarefaConfigSerializer

    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        tarefa = self.get_object()
        tarefa.ativa = True
        tarefa.save()
        return Response({'status': 'Tarefa ativada'})

    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        tarefa = self.get_object()
        tarefa.ativa = False
        tarefa.save()
        return Response({'status': 'Tarefa desativada'})




@csrf_exempt  # Desativa CSRF para permitir requisições externas
def ifood_webhook(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    # Recebe o corpo da requisição em bytes
    payload = request.body
    received_signature = request.headers.get('X-IFood-Signature')

    # Valida assinatura
    expected_signature = hmac.new(
        key=IFOOD_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(received_signature, expected_signature):
        return JsonResponse({'error': 'Assinatura inválida'}, status=403)

    try:
        data = json.loads(payload.decode('utf-8'))
        print("Evento recebido:", data)

        # Aqui você pode processar o evento, exemplo: salvar no banco

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # Responde 202 Accepted conforme requerido pelo iFood
    return HttpResponse(status=202)


@staff_member_required
def View_gerar_repasses_semanais(request):
    # Aqui vai a lógica do cálculo real — por enquanto, vamos só simular
    # Exemplo: calcular e salvar repasses para cada motoboy ativo
    print("Calculando repasses...")  # Substitua depois por lógica real

    # Mensagem de sucesso simples para admin
    return HttpResponse("Repasses semanais gerados com sucesso.")



def View_Index_Abertura(request):
    return render(request, 'index.html')  # /motopro/templates/index.html

def View_Home(request):
    return render(request, 'home.html')  # Renderiza o arquivo 'home.html'

def View_Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ou para a página desejada após o login
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def View_Logout(request):
    logout(request)
    return redirect('login')  # Redireciona após logout


def View_Dashboard(request):
    return render(request, 'login/dashboard.html')

# Usando o modelo CustomUser que você criou
# CustomUser = get_user_model()

# class UserListView(ListView):
#     model = CustomUser
#     template_name = 'users/user_list.html'
#     context_object_name = 'users'

# class UserCreateView(CreateView):
#     model = CustomUser
#     form_class = UserCreationForm
#     template_name = 'users/user_form.html'
#     success_url = reverse_lazy('user-list')

# class UserUpdateView(UpdateView):
#     model = CustomUser
#     fields = ['username', 'email', 'tipo']  # Defina os campos que você deseja editar
#     template_name = 'users/user_form.html'
#     success_url = reverse_lazy('user-list')

# class UserDeleteView(DeleteView):
#     model = CustomUser
#     template_name = 'users/user_confirm_delete.html'
#     success_url = reverse_lazy('user-list')


#####################V a g a ######################

# Listar vagas

class View_VagaList(ListView):
    model = Vaga
    template_name = 'vagas/vaga_list.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        # Usa select_related para otimizar as consultas ao contrato e estabelecimento
        return Vaga.objects.select_related('contrato__estabelecimento').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vagas = context['vagas']

        # Anexa o contrato do estabelecimento a cada vaga
        for v in vagas:
            v.contrato = Estabelecimento_Contrato.objects.filter(
                estabelecimento = v.contrato.estabelecimento if v.contrato else None
            ).first()

        context['vagas'] = vagas
        context['motoboys'] = Motoboy.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if 'salvar_vaga' in request.POST:
            vaga_id = request.POST.get("vaga_id")
            motoboy_id = request.POST.get("motoboy_id")

            try:
                vaga_obj = Vaga.objects.get(id=vaga_id)
            except Vaga.DoesNotExist:
                messages.error(request, "Vaga não encontrada.")
                return redirect('vaga-list')

            if motoboy_id:
                try:
                    motoboy_selecionado = Motoboy.objects.get(id=motoboy_id)
                    if motoboy_selecionado.status == "livre":
                        vaga_obj.motoboy = motoboy_selecionado
                        vaga_obj.save()

                        motoboy_selecionado.status = "alocado"
                        motoboy_selecionado.save()

                        messages.success(request, f"Motoboy {motoboy_selecionado} alocado com sucesso!")
                    else:
                        messages.error(request, f"Motoboy {motoboy_selecionado} já está alocado.")
                except Motoboy.DoesNotExist:
                    messages.error(request, "Motoboy não encontrado.")
            else:
                motoboy_anterior = vaga_obj.motoboy
                print("Motoboy anterior:", motoboy_anterior)

                if motoboy_anterior:
                    motoboy_anterior.status = "livre"
                    motoboy_anterior.save()
                    print(f"Status do motoboy {motoboy_anterior} após save:", motoboy_anterior.status)

                vaga_obj.motoboy = None
                vaga_obj.save()
                print("Motoboy removido da vaga:", vaga_obj.id)

                messages.success(request, "Motoboy removido da vaga.")

            return redirect('vaga-list')

        return super().post(request, *args, **kwargs)

class View_VagaCreate(CreateView):
    model         = Vaga
    form_class    = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url   = reverse_lazy('vaga-list')

# Atualizar vaga

class View_VagaUpdate(UpdateView):
    model         = Vaga
    form_class    = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url   = reverse_lazy('vaga-list')

# Excluir vaga

class View_VagaDelete(DeleteView):
    model         = Vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url   = reverse_lazy('vaga-list')


#class EstabelecimentoListView(LoginRequiredMixin,ListView):

class View_EstabelecimentoList(ListView):
    model               = Estabelecimento
    template_name       = 'estabelecimento/estabelecimento_list.html'
    context_object_name = 'estabelecimentos'


class View_EstabelecimentoCreate(CreateView):
    model          = Estabelecimento
    form_class     = EstabelecimentoForm
    template_name  = 'estabelecimento/estabelecimento_form.html'
    success_url    = reverse_lazy('estabelecimento-list')

class View_EstabelecimentoUpdate(UpdateView):
    model         = Estabelecimento
    form_class    = EstabelecimentoForm
    template_name = 'estabelecimento/estabelecimento_form.html'
    success_url   = reverse_lazy('estabelecimento-list')

class View_EstabelecimentoDelete(DeleteView):
    model         = Estabelecimento
    template_name = 'estabelecimento/estabelecimento_confirm_delete.html'
    success_url   = reverse_lazy('estabelecimento-list')

class View_MotoboyList(ListView):
    model               = Motoboy
    template_name       = 'motoboy/motoboy_list.html'
    context_object_name = 'motoboys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Motoboy._meta.get_field('status').choices  # Passa as opções de status para o template
        return context

    def post(self, request, *args, **kwargs):
        motoboys = self.get_queryset()
        for motoboy_obj in motoboys:
            # Atualizar status
            status = request.POST.get(f'status_{motoboy_obj.id}')
            if status:
                motoboy_obj.status = status
            motoboy_obj.save()  # Persistir as mudanças

        return redirect('motoboy-list')

class View_MotoboyCreate(CreateView):
    model         = Motoboy
    form_class    = MotoboyForm
    template_name = 'motoboy/motoboy_form.html'
    success_url   = reverse_lazy('motoboy-list')

class View_MotoboyUpdate(UpdateView):
    model         = Motoboy
    form_class    = MotoboyForm
    template_name = 'motoboy/motoboy_form.html'
    success_url   = reverse_lazy('motoboy-list')

class View_MotoboyDelete(DeleteView):
    model         = Motoboy
    template_name = 'motoboy/motoboy_confirm_delete.html'
    success_url   = reverse_lazy('motoboy-list')

class View_SupervisorList(ListView):
    model               = Supervisor
    template_name       = 'supervisor/supervisor_list.html'
    context_object_name = 'supervisores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Supervisor._meta.get_field('status').choices  # Passa as opções de status para o template
        return context

    def post(self, request, *args, **kwargs):
        supervisores = self.get_queryset()
        for supervisor_obj in supervisores:
            # Atualizar status
            status = request.POST.get(f'status_{supervisor_obj.id}')
            if status:
                supervisor_obj.status = status
            supervisor_obj.save()  # Persistir as mudanças

        return redirect('supervisor-list')

class View_SupervisorCreate(CreateView):
    model         = Supervisor
    form_class    = SupervisorForm
    template_name = 'supervisor/supervisor_form.html'
    success_url   = reverse_lazy('supervisor-list')


class View_SupervisorUpdate(UpdateView):
    model         = Supervisor
    form_class    = SupervisorForm
    template_name = 'supervisor/supervisor_form.html'
    success_url   = reverse_lazy('supervisor-list')

class View_SupervisorDelete(DeleteView):
    model         = Supervisor
    template_name = 'supervisor/supervisor_confirm_delete.html'
    success_url   = reverse_lazy('supervisor-list')


##class EmpresaListView(ListView):
#    model = empresa
#    template_name = 'empresa/empresa_list.html'
#    context_object_name = 'empresas'

#class EmpresaDetailView(DetailView):
#    model = empresa
#    template_name = 'empresa/empresa_detail.html'

#class EmpresaCreateView(CreateView):
#    model = empresa
#    template_name = 'empresa/empresa_form.html'
#    fields = ['nome', 'cep', 'estado_id', 'cidade_id', 'bairro_id', 'logradouro', 'numero', 'complemento', 'deadline']
#    success_url = reverse_lazy('empresa-list')

#class EmpresaUpdateView(UpdateView):
#    model = empresa
#    template_name = 'empresa/empresa_form.html'
#    fields = ['nome', 'cep', 'estado_id', 'cidade_id', 'bairro_id', 'logradouro', 'numero', 'complemento', 'deadline']
#    success_url = reverse_lazy('empresa-list')

#class EmpresaDeleteView(DeleteView):
#    model = empresa
#    template_name = 'empresa/empresa_confirm_delete.html'
#    success_url = reverse_lazy('empresa-list')    


# views.py

def minha_view(request):
    atribuir_pedido_a_motoboy(pedido_id=1, motoboy_id=2)
    rota = calcular_rota_google(["Endereço A", "Endereço B"], api_key="minha_key")
    return JsonResponse({"rota": rota})





@api_view(['POST'])
def atribuir_pedido_a_motoboy(request):
    """
    Atribui um pedido (IfoodWebhookEvent) a um motoboy.
    Espera: { "pedido_id": "...", "motoboy_id": "..." }
    """
    pedido_id = request.data.get('pedido_id')
    motoboy_id = request.data.get('motoboy_id')

    try:
        pedido = IfoodWebhookEvent.objects.get(id=pedido_id)
        motoboy = Motoboy.objects.get(id=motoboy_id)

        pedido.motoboy = motoboy
        pedido.save()

        return Response({'status': 'Pedido atribuído com sucesso'}, status=status.HTTP_200_OK)

    except IfoodWebhookEvent.DoesNotExist:
        return Response({'error': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Motoboy.DoesNotExist:
        return Response({'error': 'Motoboy não encontrado'}, status=status.HTTP_404_NOT_FOUND)




def visualizar_rota(request):
    context = {
        'api_key': 'SUA_GOOGLE_MAPS_API_KEY',
        'origem': 'Av. Paulista, 1000, São Paulo, SP',
        'destino': 'Praça da Sé, São Paulo, SP',
        'waypoints': [
            'Rua Augusta, São Paulo, SP',
            'Mercadão Municipal, São Paulo, SP'
        ]
    }
    return render(request, 'rota.html', context)
