from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from motopro.models import Vaga, Estabelecimento, Motoboy, Supervisor, Estabelecimento_Contrato
from motopro.forms import VagaForm, EstabelecimentoForm, MotoboyForm, SupervisorForm, LoginForm


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