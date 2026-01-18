import os
from pathlib import Path
from dotenv import load_dotenv # Импортируем загрузчик переменных

# Загружаем переменные из .env файла (если он есть локально)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Читаем секретный ключ из окружения. Если нет - берем дефолтный (небезопасно для продакшна, но ок для старта)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

# Читаем DEBUG. Если в env написано 'True', будет True. Иначе False.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Читаем разрешенные хосты через запятую
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'records',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'datastore.urls'

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

WSGI_APPLICATION = 'datastore.wsgi.application'

# === ГЛАВНОЕ ИЗМЕНЕНИЕ: БАЗА ДАННЫХ ===
# Теперь мы подключаемся к PostgreSQL
# Проверяем, есть ли переменная DB_HOST (она есть только в Docker/Production)
if os.environ.get('DB_HOST'):
    # Настройки для DOCKER (PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'postgres'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # Настройки для ЛОКАЛЬНОЙ разработки (SQLite)
    print("⚠️ Используется локальная база SQLite (Docker не обнаружен)")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Настройки статики (важно для Docker)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Сюда соберется вся статика

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'