import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

env_conf = load_dotenv()
if not env_conf:
    raise FileNotFoundError("File .env not found.")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    # Встроенные модули Django.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Сторонние модули.
    "rest_framework",  # REST Framework.
    "rest_framework_simplejwt",  # REST Framework auth.
    "drf_yasg",  # Documentation for API.
    # Модули приложения.
    "apps.authorization",  # Custom auth module.
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


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

# WSGI settings.
WSGI_APPLICATION = "core.wsgi.application"

# Urls settings.
ROOT_URLCONF = "core.urls"
API_BASE_URL = "api/v1/"
STATIC_URL = "static/"

# CSRF
CSRF_USE_SESSIONS = False
# CSRF_COOKIE_AGE = 604800  # 604800 - one week
CSRF_HEADERS_NAME = "X-CSRFToken"

# Authentication/authorization settings.
ACCESS_TOKEN_LIFETIME = int(os.getenv("LIFETIME_ACCESS"))
REFRESH_TOKEN_LIFETIME = int(os.getenv("LIFETIME_REFRESH"))
JWT_AUTH = "rest_framework_simplejwt.authentication."

AUTH_USER_MODEL = "authorization.User"
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
    # Одноразовый ли refresh_token.
    "ROTATE_REFRESH_TOKENS": False,
    # Добавлять ли одноразовый refresh_token в черный список.
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",  # для RSA: RS256, RS384 или RS512
    "SIGNING_KEY": SECRET_KEY,  # в RSA это приватный ключ
    "VERIFYING_KEY": None,  # в RSA это публичный ключ
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": JWT_AUTH + "default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # custom
    "AUTH_COOKIE_DOMAIN": None,
    "AUTH_COOKIE_SECURE": False,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",  # The path of the auth cookie.
    "AUTH_COOKIE_SAME_SITE": "Lax",
}
if SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
    INSTALLED_APPS.append("rest_framework_simplejwt.token_blacklist")

# Databases settings.
LOCAL_TESTING_DATABASE = {  # Local database for testing.
    "testing": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testing",
        "USER": "test",
        "PASSWORD": "test",
        "HOST": "postgres_for_tests",
        "PORT": 5432,
    },
}
PROD_DATABASES = {  # Remote production database.
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PROD_DATABASE_NAME"),
        "USER": os.getenv("PROD_DATABASE_USER"),
        "PASSWORD": os.getenv("PROD_DATABASE_PASSWORD"),
        "HOST": os.getenv("PROD_DATABASE_HOST"),
        "PORT": int(os.getenv("PROD_DATABASE_PORT")),
    },
}
DEVELOPMENT_DATABASES = {  # Remote copy of production database.
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     "NAME": os.getenv("DEVELOPMENT_DATABASE_NAME"),
    #     "USER": os.getenv("DEVELOPMENT_DATABASE_USER"),
    #     "PASSWORD": os.getenv("DEVELOPMENT_DATABASE_PASSWORD"),
    #     "HOST": os.getenv("DEVELOPMENT_DATABASE_HOST"),
    #     "PORT": int(os.getenv("DEVELOPMENT_DATABASE_PORT")),
    # },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    **LOCAL_TESTING_DATABASE,
}
DATABASES = DEVELOPMENT_DATABASES if DEBUG else PROD_DATABASES
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Default pk field type.

# Caches settings.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("LOCATION_CACHE"),
        "OPTIONS": {
            "TIMEOUT": 600,
            "MAX_ENTRIES": 100,
        },
    },
}

# Logging settings.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s",
        },
        "simple": {
            "class": "logging.Formatter",
            "format": "%(levelname)s >> %(message)s",
        },
        "base": {
            "format": (
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s - %(module)s | "
                "%(message)s"
            ),
        },
        "testing": {
            "format": (
                "%(asctime)s | "
                "Module: %(module)s | "
                "Func: %(funcName)s | "
                "Line: %(lineno)d | "
                "%(message)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
        "console_testing": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "testing",
        },
        "console_short": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console"],
            "propagate": False,
            "level": "INFO",
        },
        "testing": {
            "handlers": ["console_testing"],
            "propagate": False,
            "level": "DEBUG",
        },
        "app": {
            "handlers": ["console"],
            "propagate": False,
            "level": "DEBUG",
        },
    },
}

# DRF settings.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# Celery settings.
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_BROKER_CONNECTION_RETRY = 5
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = 5
CELERY_TIMEZONE = "Europe/Moscow"

# Password validation.
VALIDATOR = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": VALIDATOR + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": VALIDATOR + "MinimumLengthValidator",
    },
    {
        "NAME": VALIDATOR + "CommonPasswordValidator",
    },
    {
        "NAME": VALIDATOR + "NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
