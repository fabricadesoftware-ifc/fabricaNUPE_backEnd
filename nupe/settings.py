import os
from datetime import timedelta

import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", bool, False)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # terceiros
    "rest_framework",
    "oauth2_provider",
    "safedelete",
    "drf_yasg",
    "django_filters",
    "corsheaders",
    # apps
    "nupe.core",
    "nupe.file",
    "nupe.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

ROOT_URLCONF = "nupe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nupe.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    # autenticação
    "DEFAULT_AUTHENTICATION_CLASSES": ("oauth2_provider.contrib.rest_framework.OAuth2Authentication",),
    "DEFAULT_PERMISSION_CLASSES": ("drf_action_permissions.DjangoActionPermissions",),
    # render/parser
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    # filtros
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # paginação
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # testes
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "NUPE Authentication": {"type": "oauth2", "tokenUrl": "/oauth/token/", "flow": "password"}
    },
    "DEFAULT_INFO": "nupe.urls.api_info",
}

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": timedelta(hours=4).seconds,
    "REFRESH_TOKEN_EXPIRE_SECONDS": timedelta(hours=8).seconds,
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
}

DATABASES = {"default": env.db()}

AUTH_USER_MODEL = "account.Account"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_URL = "/media/"
