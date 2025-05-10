from django.contrib import admin
from django.urls import path, include, re_path
from api_v01.views  import LoginView
from django.conf import settings
from django.views.static import serve

from motopro.views import View_VagaCreate, View_VagaUpdate, View_VagaDelete
from motopro.views import View_EstabelecimentoCreate, View_EstabelecimentoUpdate, View_EstabelecimentoDelete, View_EstabelecimentoList
from motopro.views import View_MotoboyCreate, View_MotoboyUpdate, View_MotoboyDelete, View_MotoboyList
from motopro.views import View_SupervisorCreate, View_SupervisorUpdate, View_SupervisorDelete, View_SupervisorList
from motopro.views import View_VagaList 
from motopro.views import View_Index_Abertura, View_Home, View_Logout, View_Login 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", View_Index_Abertura, name="index"),  # Defina o  como rota padrão
    path('home/', View_Home, name='home'),

    path('', include('motopro.urls')),  # Garante que urls do app estão ativas

    path('admin/',  admin.site.urls),
    re_path('api/v1/', include('api_v01.urls')),  # Inclui todas as APIs na pasta api_v01
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
       
    path('login/',  View_Login, name='login'),
    path('logout/', View_Logout, name='logout'),
 
    path('accounts/', include('django.contrib.auth.urls')),  # Inclui URLs de login, logout, etc.
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

 


########## vagas ################
    path('vagas/',                 View_VagaList.as_view(),   name='vaga-list'),
    path('vagas/create/',          View_VagaCreate.as_view(), name='vaga-create'),
    path('vagas/update/<int:pk>/', View_VagaUpdate.as_view(), name='vaga-update'),
    path('vagas/delete/<int:pk>/', View_VagaDelete.as_view(), name='vaga-delete'),
########## Motoboy ################   
    path('motoboy',                  View_MotoboyList.as_view(), name='motoboy-list'),
    path('motoboy/create/',          View_MotoboyCreate.as_view(), name='motoboy-create'),
    path('motoboy/update/<int:pk>/', View_MotoboyUpdate.as_view(), name='motoboy-update'),
    path('motoboy/delete/<int:pk>/', View_MotoboyDelete.as_view(), name='motoboy-delete'),
########## Supervisor ################
    path('supervisor/',                 View_SupervisorList.as_view(), name='supervisor-list'),
    path('supervisor/create/',          View_SupervisorCreate.as_view(), name='supervisor-create'),
    path('supervisor/update/<int:pk>/', View_SupervisorUpdate.as_view(), name='supervisor-update'),
    path('supervisor/delete/<int:pk>/', View_SupervisorDelete.as_view(), name='supervisor-delete'),
########## Estabelecimentos ################
    path('estabelecimentos/',                 View_EstabelecimentoList.as_view(), name='estabelecimento-list'),
    path('estabelecimentos/create/',          View_EstabelecimentoCreate.as_view(), name='estabelecimento-create'),
    path('estabelecimentos/update/<int:pk>/', View_EstabelecimentoUpdate.as_view(), name='estabelecimento-update'),
    path('estabelecimentos/delete/<int:pk>/', View_EstabelecimentoDelete.as_view(), name='estabelecimento-delete'),

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



