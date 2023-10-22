from .base import *

# Configurações específicas para testes
DEBUG = False  # Desativa o modo de depuração durante os testes

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',  # Usa um banco de dados SQLite em memória para os testes
}

# Configurações para acelerar os testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Configurações de cache
CACHES = {
    'default': {
        # Usa um cache fictício durante os testes
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
