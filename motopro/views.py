from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from motopro.models import vaga, estabelecimento, motoboy, supervisor
from motopro.forms import VagaForm, EstabelecimentoForm, MotoboyForm, SupervisorForm, LoginForm  



def dashboard(request):
    return render(request, 'login/dashboard.html')


def login_view(request):
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


def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona após logout

def index(request):
    return render(request, 'index.html')

@login_required
def home_view(request):
    return render(request, 'home.html')  # Renderiza o arquivo 'home.html'

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


class VagaListView(ListView):
    model = vaga
    template_name = 'vagas/vaga_list.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        filtro = self.request.GET.get('filtro', 'todas')

        if filtro == 'abertas':
            return vaga.objects.filter(motoboy__isnull=True)
        elif filtro == 'alocadas':
            return vaga.objects.filter(motoboy__isnull=False)
        else:
            return vaga.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['motoboys'] = motoboy.objects.all()
   
    
        return context
    
    
    def post(self, request, *args, **kwargs):
        # Verifica se o botão "Salvar Todos" foi pressionado
        if 'save_all' in request.POST:
            for vaga in self.get_queryset():
                motoboy_id = request.POST.get(f"motoboy_{vaga.id}")
                
                if motoboy_id:
                    try:
                        motoboy_selecionado = motoboy.objects.get(id=motoboy_id)
                        # Verificar se o motoboy está livre antes de alocar
                        if motoboy_selecionado.status == "livre":
                            # Alocar motoboy à vaga
                            vaga.motoboy = motoboy_selecionado
                            vaga.save()

                            # Atualizar o status do motoboy para "alocado"
                            motoboy_selecionado.status = "alocado"
                            motoboy_selecionado.save()
                        else:
                            messages.error(request, f"O motoboy {motoboy_selecionado} já está alocado em outra vaga.")
                    except motoboy.DoesNotExist:
                        messages.error(request, f"Motoboy com ID {motoboy_id} não encontrado.")
                else:
                    # Se não houver motoboy selecionado, deixar a vaga sem motoboy
                    vaga.motoboy = None
                    vaga.save()

            # Após a atualização, redireciona para a mesma página
            return redirect('vaga-list')

        return super().post(request, *args, **kwargs)

# Criar vaga

class VagaCreateView(CreateView):
    model         = vaga
    form_class    = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url   = reverse_lazy('vaga-list')

# Atualizar vaga

class VagaUpdateView(UpdateView):
    model         = vaga
    form_class    = VagaForm
    template_name = 'vagas/vaga_form.html'
    success_url   = reverse_lazy('vaga-list')

# Excluir vaga

class VagaDeleteView(DeleteView):
    model         = vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url   = reverse_lazy('vaga-list')


#class EstabelecimentoListView(LoginRequiredMixin,ListView):

class EstabelecimentoListView(ListView):
    model               = estabelecimento
    template_name       = 'estabelecimento/estabelecimento_list.html'
    context_object_name = 'estabelecimentos'


class EstabelecimentoCreateView(CreateView):
    model          = estabelecimento
    form_class     = EstabelecimentoForm
    template_name  = 'estabelecimento/estabelecimento_form.html'
    success_url    = reverse_lazy('estabelecimento-list')


class EstabelecimentoUpdateView(UpdateView):
    model         = estabelecimento
    form_class    = EstabelecimentoForm
    template_name = 'estabelecimento/estabelecimento_form.html'
    success_url   = reverse_lazy('estabelecimento-list')


class EstabelecimentoDeleteView(DeleteView):
    model         = estabelecimento
    template_name = 'estabelecimento/estabelecimento_confirm_delete.html'
    success_url   = reverse_lazy('estabelecimento-list')

class MotoboyListView(ListView):
    model               = motoboy
    template_name       = 'motoboy/motoboy_list.html'
    context_object_name = 'motoboys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = motoboy._meta.get_field('status').choices  # Passa as opções de status para o template
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

class MotoboyCreateView(CreateView):
    model         = motoboy
    form_class    = MotoboyForm
    template_name = 'motoboy/motoboy_form.html'
    success_url   = reverse_lazy('motoboy-list')

class MotoboyUpdateView(UpdateView):
    model         = motoboy
    form_class    = MotoboyForm
    template_name = 'motoboy/motoboy_form.html'
    success_url   = reverse_lazy('motoboy-list')

class MotoboyDeleteView(DeleteView):
    model         = motoboy
    template_name = 'motoboy/motoboy_confirm_delete.html'
    success_url   = reverse_lazy('motoboy-list')

class SupervisorListView(ListView):
    model               = supervisor
    template_name       = 'supervisor/supervisor_list.html'
    context_object_name = 'supervisores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = supervisor._meta.get_field('status').choices  # Passa as opções de status para o template
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

class SupervisorCreateView(CreateView):
    model         = supervisor
    form_class    = SupervisorForm
    template_name = 'supervisor/supervisor_form.html'
    success_url   = reverse_lazy('supervisor-list')


class SupervisorUpdateView(UpdateView):
    model         = supervisor
    form_class    = SupervisorForm
    template_name = 'supervisor/supervisor_form.html'
    success_url   = reverse_lazy('supervisor-list')


class SupervisorDeleteView(DeleteView):
    model         = supervisor
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