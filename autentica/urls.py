from django.contrib import admin
from django.urls import path, include, re_path
from api_v01.views  import LoginView
from django.conf import settings
from django.views.static import serve


from motopro.views import index, home_view 
from motopro.views import VagaCreateView, VagaUpdateView, VagaDeleteView
from motopro.views import EstabelecimentoCreateView, EstabelecimentoUpdateView, EstabelecimentoDeleteView, EstabelecimentoListView
from motopro.views import MotoboyCreateView, MotoboyUpdateView, MotoboyDeleteView, MotoboyListView
from motopro.views import SupervisorCreateView, SupervisorUpdateView, SupervisorDeleteView, SupervisorListView
from motopro.views import VagaListView  # Certifique-se de que está importando a classe corretamente

from motopro.views import login_view, logout_view


from django.contrib.auth import views as auth_views






urlpatterns = [
    path("", index, name="index"),  # Defina a home como rota padrão
   
    path('home/', home_view, name='home'),
   
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    re_path('api/v1/', include('api_v01.urls')),  # Inclui todas as APIs na pasta api_v01
   
    path('login/',   login_view, name='login'),
    path('logout/',  logout_view, name='logout'),
    path('admin/',   admin.site.urls),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

########## vagas ################
    path('vagas/',                 VagaListView.as_view(),   name='vaga-list'),
    path('vagas/create/',          VagaCreateView.as_view(), name='vaga-create'),
    path('vagas/update/<int:pk>/', VagaUpdateView.as_view(), name='vaga-update'),
    path('vagas/delete/<int:pk>/', VagaDeleteView.as_view(), name='vaga-delete'),
########## Motoboy ################   
    path('motoboy', MotoboyListView.as_view(), name='motoboy-list'),
    path('motoboy/create/', MotoboyCreateView.as_view(), name='motoboy-create'),
    path('motoboy/update/<int:pk>/', MotoboyUpdateView.as_view(), name='motoboy-update'),
    path('motoboy/delete/<int:pk>/', MotoboyDeleteView.as_view(), name='motoboy-delete'),
########## Supervisor ################
    path('supervisor/', SupervisorListView.as_view(), name='supervisor-list'),
    path('supervisor/create/', SupervisorCreateView.as_view(), name='supervisor-create'),
    path('supervisor/update/<int:pk>/', SupervisorUpdateView.as_view(), name='supervisor-update'),
    path('supervisor/delete/<int:pk>/', SupervisorDeleteView.as_view(), name='supervisor-delete'),
########## Estabelecimentos ################
    path('estabelecimentos/', EstabelecimentoListView.as_view(), name='estabelecimento-list'),
    path('estabelecimentos/create/', EstabelecimentoCreateView.as_view(), name='estabelecimento-create'),
    path('estabelecimentos/update/<int:pk>/', EstabelecimentoUpdateView.as_view(), name='estabelecimento-update'),
    path('estabelecimentos/delete/<int:pk>/', EstabelecimentoDeleteView.as_view(), name='estabelecimento-delete'),

    ########## Empesas ################
 #    path('empresas/',                EmpresaListView.as_view(),   name='empresa-list'),  # Lista de empresas
 #    path('empresa/<int:pk>/',        EmpresaDetailView.as_view(), name='empresa-detail'),  # Detalhe de uma empresa
 #    path('empresa/create/',          EmpresaCreateView.as_view(), name='empresa-create'),  # Criação de empresa
 #    path('empresa/<int:pk>/update/', EmpresaUpdateView.as_view(), name='empresa-update'),  # Atualização de empresa
 #    path('empresa/<int:pk>/delete/', EmpresaDeleteView.as_view(), name='empresa-delete'),  # Exclusão de empresa
  
    ######### users   ####################
 #    path('users/',                 UserListView.as_view(),   name='user-list'),
 #    path('users/create/',          UserCreateView.as_view(), name='user-create'),
 #    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
 #    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
   
]



