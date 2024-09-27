import os
import urllib.parse as urlparse  # For parsing Redis URL
from pathlib import Path
import django_heroku  # For Heroku settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'battletrivia-53f5e19174e5.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'social_django',
    'corsheaders',
    'channels',  # Added channels
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'trivia_backend.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Changed from WSGI to ASGI for Channels support
WSGI_APPLICATION = 'trivia_backend.wsgi.application'
ASGI_APPLICATION = 'trivia_backend.asgi.application'  # Added ASGI application path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'your_db_name'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', '123'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_TWITCH_KEY = os.getenv('TWITCH_CLIENT_ID')
SOCIAL_AUTH_TWITCH_SECRET = os.getenv('TWITCH_SECRET')
TWITCH_REDIRECT_URI = os.getenv('TWITCH_REDIRECT_URI', 'http://localhost:8000/auth/complete/twitch/')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitch.TwitchOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Extract REDIS_URL from Heroku environment variables or use local settings
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

urlparse.uses_netloc.append('redis')
redis_conf = urlparse.urlparse(redis_url)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_conf.hostname, redis_conf.port)],
            "password": redis_conf.password,  # Include password if available in URL
        },
    },
}

LOGIN_REDIRECT_URL = '/save_twitch_channel/'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

CORS_ORIGIN_ALLOW_ALL = True

# Activate Django-Heroku settings for database and static files
django_heroku.settings(locals())
