from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

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
            return Response({'token': token.key}, status=HTTP_200_OK)

        return Response({'error': 'Invalid email or password'}, status=HTTP_401_UNAUTHORIZED)
