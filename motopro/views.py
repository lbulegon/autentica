from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from motopro.models import vaga
from motopro.forms import VagaForm


from motopro.models import estabeleciomento
from motopro.forms import EstabelecimentoForm

from motopro.models import motoboy
from motopro.forms import MotoboyForm

from motopro.models import supervisor
from motopro.forms import SupervisorForm


def home(request):
     return render(request, 'home.html')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['motoboys'] = motoboy.objects.all()  # Passa a lista de motoboys para o template
        return context

    def post(self, request, *args, **kwargs):
        vagas = self.get_queryset()
        for vaga_obj in vagas:
            # Atualizar motoboy
            motoboy_id = request.POST.get(f'motoboy_{vaga_obj.id}')
            if motoboy_id:  # Se motoboy_id não estiver vazio
                try:
                    motoboy_obj = motoboy.objects.get(id=motoboy_id)
                    vaga_obj.motoboy_id = motoboy_obj  # Atribua a instância do motoboy
                except motoboy.DoesNotExist:
                    vaga_obj.motoboy_id = None  # Se o motoboy não existir, definir como None
            else:
                vaga_obj.motoboy_id = None  # Se nenhum motoboy for selecionado, definimos como None

            # Atualizar status
            status = request.POST.get(f'status_{vaga_obj.id}')
            if status:
                vaga_obj.status = status

            vaga_obj.save()  # Persistir a vaga com as novas mudanças

        return redirect('vaga-list')
    

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

class EstabelecimentoListView(LoginRequiredMixin,ListView):
    model               = estabeleciomento
    template_name       = 'estabelecimento/estabelecimento_list.html'
    context_object_name = 'estabelecimentos'

class EstabelecimentoCreateView(CreateView):
    model          = estabeleciomento
    form_class     = EstabelecimentoForm
    template_name  = 'estabelecimento/estabelecimento_form.html'
    success_url    = reverse_lazy('estabelecimento-list')

class EstabelecimentoUpdateView(UpdateView):
    model         = estabeleciomento
    form_class    = EstabelecimentoForm
    template_name = 'estabelecimento/estabelecimento_form.html'
    success_url   = reverse_lazy('estabelecimento-list')

class EstabelecimentoDeleteView(DeleteView):
    model         = estabeleciomento
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