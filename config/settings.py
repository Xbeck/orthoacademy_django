import os
import environ
from pathlib import Path



env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*', env('DNS_SERVER'), env('DNS_WWW_1'), env('DNS_1'), env('DNS_WWW_2'), env('DNS_2'), '127.0.0.1']

LOGIN_URL = "users:login"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tashqi paket
    "crispy_forms",
    "crispy_bootstrap5",
    # 'ckeditor',
    # 'ckeditor-uploader',
    'rest_framework',

    # men yaratgan applar
    'users',
    'courses',
    # 'payme',
    ]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'users.middleware.SimpleMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          BASE_DIR / "templates",
          # BASE_DIR / "business",
          # BASE_DIR / "professions/templates/professions",
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    # PostgreSQL uchun
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
      }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "users.CustomUser"

MEDIA_URL = "/media/"
MEDIA_ROOT = "media-files"

MEDIAFILES_DIRS = [
      BASE_DIR / 'media-files',
      ]

STATIC_URL = 'static/'

STATIC_ROOT = 'static-files'

STATICFILES_DIRS = [
      BASE_DIR / 'static',
      # BASE_DIR / 'static/images',
]


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# # EMAIL_HOST_USER = 'test@gmail.com'
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# # EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# Payme configurations
PAYME: dict = {
    'PAYME_ID': env('PAYME_ID'),
    'PAYME_KEY': env('PAYME_KEY'),
    'PAYME_URL': env('PAYME_URL'),
    'PAYME_CALL_BACK_URL': env('PAYME_CALL_BACK_URL'),
    'PAYME_MIN_AMOUNT': env('PAYME_MIN_AMOUNT'),
    'PAYME_ACCOUNT': env('PAYME_ACCOUNT'),
}

ORDER_MODEL = 'user.models.Order'