from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from django.shortcuts import render

class LoginView(APIView):
    """
    API para autenticação usando email e senha.
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Autentica o usuário pelo email
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Retorna ou gera um token para o usuário autenticado
            token, _ = Token.objects.get_or_create(user=user)

            # Inclui os campos adicionais do User
            user_data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            }
            return Response(user_data, status=HTTP_200_OK)

        return Response({'error': 'Invalid email or password'}, status=HTTP_401_UNAUTHORIZED)

def home_view(request):
    return render(request, 'home.html', {})
