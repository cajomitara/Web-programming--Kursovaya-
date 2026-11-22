"""
Настройки сервиса авторизации.

Сервис владеет учётными записями пользователей (своя БД),
выдаёт JWT-токены при входе и предоставляет внутренний API
для других сервисов (создание и переименование пользователей).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-auth-service-dev-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
# "auth" — имя сервиса в docker compose / Kubernetes: по нему к нам обращается backend
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,auth").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auth_project.wsgi.application'

# Собственная база данных сервиса (принцип «база данных на сервис»)
if os.environ.get("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "auth"),
            "USER": os.environ.get("DB_USER", "auth"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DB_PATH", BASE_DIR / "auth.sqlite3"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

# Админка сервиса живёт по пути /auth/admin/, её статика — /auth/static/,
# чтобы не пересекаться с админкой и статикой основного backend через шлюз
STATIC_URL = '/auth/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Cookie сессии и CSRF админки ограничены путём /auth/,
# чтобы не перезаписывать одноимённые cookie админки основного backend
SESSION_COOKIE_PATH = '/auth/'
CSRF_COOKIE_PATH = '/auth/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- JWT ---
# Общий секрет, которым сервис подписывает токены, а backend их проверяет
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-jwt-secret-change-me")
JWT_LIFETIME_SECONDS = int(os.environ.get("JWT_LIFETIME_SECONDS", 8 * 60 * 60))
JWT_COOKIE_NAME = "access_token"

# --- Внутренний API ---
# Токен, который другие сервисы передают в заголовке X-Service-Token
SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN", "dev-service-token")
