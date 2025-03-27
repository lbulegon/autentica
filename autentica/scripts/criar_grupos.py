import os
import django

# Configurando o Django para rodar fora do ambiente web
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autentica.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from motopro.models import Vaga, Motoboy, Empresa, Candidatura  # Ajuste conforme os modelos reais do seu projeto

# Criando os grupos de usuários
grupos = {
    "Admin": ["add_vaga", "change_vaga", "delete_vaga", "view_vaga",
              "add_motoboy", "change_motoboy", "delete_motoboy", "view_motoboy",
              "add_empresa", "change_empresa", "delete_empresa", "view_empresa",
              "add_candidatura", "change_candidatura", "delete_candidatura", "view_candidatura"],
    
    "Empresa": ["add_vaga", "change_vaga", "view_vaga",
                "view_motoboy", "view_empresa", "add_candidatura", "view_candidatura"],

    "Motoboy": ["view_vaga", "add_candidatura", "view_candidatura"],
}

# Criando os grupos e adicionando as permissões
for nome_grupo, permissoes in grupos.items():
    grupo, created = Group.objects.get_or_create(name=nome_grupo)
    for perm in permissoes:
        try:
            nome_modelo = perm.split('_')[-1]
            content_type = ContentType.objects.get(model=nome_modelo)
            permissao = Permission.objects.get(codename=perm, content_type=content_type)
            grupo.permissions.add(permissao)
        except Exception as e:
            print(f"Erro ao adicionar permissão {perm} ao grupo {nome_grupo}: {e}")

print("Grupos criados com sucesso! 🎉")
