from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-9n2lmrvscun5g0)!*(v$u-ya^i8def_=+ad917=i9djz*kd&px'
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    # Встроенные модули Django.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние модули.
    'rest_framework',                       # REST Framework.
    'rest_framework_simplejwt',             # REST Framework auth.
    'drf_yasg',                             # Documentation for API.

    # Модули приложения.
    'apps.authorization',                   # Custom auth module.
    'apps.storage',                         # Storage for files.
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

# WSGI settings.
WSGI_APPLICATION = 'core.wsgi.application'

# Urls settings.
ROOT_URLCONF = 'core.urls'
API_BASE_URL = 'api/v1/'
STATIC_URL = 'static/'

# Authentication/authorization settings.
AUTH_USER_MODEL = 'authorization.User'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Databases settings.
LOCAL_TESTING_DATABASE = {                  # Local database for testing.
    'testing': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
PROD_DATABASES = {                          # Remote production database.
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'postgres',
        'PORT': 5432,
    },
    **LOCAL_TESTING_DATABASE,
}
LOCAL_DATABASES = {                         # Remote copy of production database.
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': '220',
    #     'USER': 'admin',
    #     'PASSWORD': 'admin',
    #     'HOST': 'postgres',
    #     'PORT': 5432,
    # },
    # **LOCAL_TESTING_DATABASE,
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
DATABASES = LOCAL_DATABASES if DEBUG else PROD_DATABASES
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'    # Default pk field type.

# Caches settings.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379',
        'OPTIONS': {
            'TIMEOUT': 600,
            'MAX_ENTRIES': 100,
        }
    }
}

# Logging settings.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(levelname)s >> %(message)s',
        },
        'base': {
            'format': (
                '%(asctime)s | '
                '%(levelname)s | '
                '%(name)s - %(module)s | '
                '%(message)s'
            ),
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base',
        },
        'console_short': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'app': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },

    },
}

# DRF settings.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
      'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ]
}

# Celery settings.
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_BROKER_CONNECTION_RETRY = 5
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = 5
CELERY_TIMEZONE = 'Europe/Moscow'

# Password validation.
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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
