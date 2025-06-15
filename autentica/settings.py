from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lxh3b=6@xx(h#6)uhw++a)cre=^!l##^mf%*lolt*3ge0@4flu'

# SECURITY WARNING: don't run with debug turned on in production! 
#ALLOWED_HOSTS = ['192.168.0.18','localhost', '127.0.0.1', '192.168.0.30']
ALLOWED_HOSTS = [
    'autentica-production.up.railway.app',
    'autentica-desenvolvimento.up.railway.app',
    '127.0.0.1',  # Opcional: Para testes locais
    'localhost',  # Opcional: Para testes locais  
    '192.168.0.30', 
]

CSRF_TRUSTED_ORIGINS = ['https://autentica-desenvolvimento.up.railway.app','https://autentica-production.up.railway.app']
DJANGO_ALLOWED_HOSTS = ['autentica-production.up.railway.app','autentica-desenvolvimento.up.railway.app']
STATIC_URL           = '/static/'
# Se você estiver em ambiente de produção e precisar servir arquivos estáticos, use esta configuração:
STATICFILES_DIRS = [ BASE_DIR / "static",]  # Se estiver usando o caminho BASE_DIR
# Para produção, você também pode precisar de:
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_PERMISSION_CLASSES: [ 'rest_framework.permissions.AllowAny',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'api_v01',
    'motopro',    
    'corsheaders',   
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <-- deve ser o primeiro middleware externo
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Para desenvolvimento
    ],
}


ROOT_URLCONF = 'autentica.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'autentica.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql',     # Define o backend do PostgreSQL
        'NAME'     : 'railway',                           # Nome do banco de dados
        'USER'     : 'postgres',                          # Usuário do banco de dados
        'PASSWORD' : 'smivcxktjtChwExHSrVbiAFWgfZkmDrS',  # Senha do banco de dados
        'HOST'     : 'junction.proxy.rlwy.net',           # Host (o container está mapeado para localhost)
        'PORT'     : '57279',                             # Porta padrão do PostgreSQL
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Define o backend do PostgreSQL
        'NAME': 'motopro',  # Nome do banco de dados
        'USER': 'postgres',  # Usuário do banco de dados
        'PASSWORD': '1234',  # Senha do banco de dados
        'HOST': 'localhost',  # Host (o container está mapeado para localhost)
        'PORT': '5432',  # Porta padrão do PostgreSQL
    }
}

"""

"""
# busca no arquivo .env

print("DB NAME:", config('DB_NAME'))  # Deve mostrar: DB NAME: railway

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

"""
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'
#AUTH_USER_MODEL     = 'motopro.CustomUser'
AUTHENTICATION_BACKENDS = [
    'api_v01.backends.EmailBackend',              # Nosso backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão (opcional)
]

LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL  = 'home'  # Redireciona para a página 'home' após o login
LOGOUT_REDIRECT_URL = 'login'  # Redireciona para a página de login após o logout

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_TASK_TRACK_STARTED = True    

DEBUG = True

# Configurações do meu programa residente
MY_PROGRAM_CONFIG = {
    'INTERVAL': 15,  # Intervalo padrão de 15 segundos
    'ENABLE_LOG': True,
    'EXECUTION_TIMES': ['08:00', '14:00', '20:00'],
    'LOG_FILE': '/tmp/meuprograma.log'
}

GOOGLE_MAPS_API_KEY  = 'AIzaSyD30AKY4fZlu-RaYu6FQBuWBVxgyauhXw4'
IFOOD_WEBHOOK_SECRET = 'b4fbef0a8a703123ea95219c66b88fb4c69c638879cedc10714628dbf0673655'