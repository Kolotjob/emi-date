# Удалите или закомментируйте:
WSGI_APPLICATION = 'dj_emi.wsgi.application'

# Добавьте:
ASGI_APPLICATION = 'dj_emi.asgi.application'

ROOT_URLCONF = 'dj_emi.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Ваши приложения:
    'profile__card',
]