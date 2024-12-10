from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lxh3b=6@xx(h#6)uhw++a)cre=^!l##^mf%*lolt*3ge0@4flu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['192.168.0.18','localhost', '127.0.0.1', '192.168.0.30']
ALLOWED_HOSTS = [
    'autentica-production.up.railway.app',
    '127.0.0.1',  # Opcional: Para testes locais
    'localhost',  # Opcional: Para testes locais
    '192.168.0.30',
    'autentica-desenvolvimento.up.railway.app'
]
CSRF_TRUSTED_ORIGINS = ['https://autentica-desenvolvimento.up.railway.app','https://autentica-production.up.railway.app']

DJANGO_ALLOWED_HOSTS = ['autentica-production.up.railway.app','autentica-desenvolvimento.up.railway.app']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api_v01',
    'motopro',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'autentica.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
        'ENGINE': 'django.db.backends.postgresql',  # Define o backend do PostgreSQL
        'NAME': 'railway',  # Nome do banco de dados
        'USER': 'postgres',  # Usuário do banco de dados
        'PASSWORD': 'smivcxktjtChwExHSrVbiAFWgfZkmDrS',  # Senha do banco de dados
        'HOST': 'junction.proxy.rlwy.net',  # Host (o container está mapeado para localhost)
        'PORT': '57279',  # Porta padrão do PostgreSQL
    }
}


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',  # Define o backend do PostgreSQL
#        'NAME': 'lbulegon',  # Nome do banco de dados
#        'USER': 'lbulegon',  # Usuário do banco de dados
#        'PASSWORD': 'ljb#215195',  # Senha do banco de dados
#        'HOST': 'localhost',  # Host (o container está mapeado para localhost)
#        'PORT': '5432',  # Porta padrão do PostgreSQL
#    }
#}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#AUTH_USER_MODEL     = 'motopro.CustomUser'

AUTHENTICATION_BACKENDS = [
    'api_v01.backends.EmailBackend',  # Nosso backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão (opcional)
]

