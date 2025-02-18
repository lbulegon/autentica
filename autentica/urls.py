"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from api_v01.views  import LoginView, home_view
from django.conf import settings
from django.views.static import serve

from motopro.views import home 
from motopro.views import VagaCreateView, VagaUpdateView, VagaDeleteView,VagaListView
from motopro.views import EstabelecimentoCreateView, EstabelecimentoUpdateView, EstabelecimentoDeleteView, EstabelecimentoListView
from motopro.views import MotoboyCreateView, MotoboyUpdateView, MotoboyDeleteView, MotoboyListView


urlpatterns = [
    
    path("", home_view, name="home"),  # Defina a home como rota padrão
    path('admin/',     admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('login/',     LoginView.as_view(), name='login'),
   
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

   
    ######### users   ####################
 #   path('users/',                 UserListView.as_view(),   name='user-list'),
 #    path('users/create/',          UserCreateView.as_view(), name='user-create'),
  #   path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
  #   path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
   
   ########## vagas ################
     path('vagas/',                 VagaListView.as_view(),   name='vaga-list'),
     path('vagas/create/',          VagaCreateView.as_view(), name='vaga-create'),
     path('vagas/update/<int:pk>/', VagaUpdateView.as_view(), name='vaga-update'),
     path('vagas/delete/<int:pk>/', VagaDeleteView.as_view(), name='vaga-delete'),

    ########## Empesas ################
  #   path('empresas/',                EmpresaListView.as_view(),   name='empresa-list'),  # Lista de empresas
 #    path('empresa/<int:pk>/',        EmpresaDetailView.as_view(), name='empresa-detail'),  # Detalhe de uma empresa
 #    path('empresa/create/',          EmpresaCreateView.as_view(), name='empresa-create'),  # Criação de empresa
 #    path('empresa/<int:pk>/update/', EmpresaUpdateView.as_view(), name='empresa-update'),  # Atualização de empresa
 #    path('empresa/<int:pk>/delete/', EmpresaDeleteView.as_view(), name='empresa-delete'),  # Exclusão de empresa

    # Estabelecimentos
    path('estabelecimentos/', EstabelecimentoListView.as_view(), name='estabelecimento-list'),
    path('estabelecimentos/create/', EstabelecimentoCreateView.as_view(), name='estabelecimento-create'),
    path('estabelecimentos/update/<int:pk>/', EstabelecimentoUpdateView.as_view(), name='estabelecimento-update'),
    path('estabelecimentos/delete/<int:pk>/', EstabelecimentoDeleteView.as_view(), name='estabelecimento-delete'),
    
    path('motoboy', MotoboyListView.as_view(), name='motoboy-list'),
    path('motoboy/create/', MotoboyCreateView.as_view(), name='motoboy-create'),
    path('motoboy/<int:pk>/', MotoboyUpdateView.as_view(), name='motoboy-update'),
    path('motoboy/<int:pk>/', MotoboyDeleteView.as_view(), name='motoboy-delete'),

]

