"""
Django settings for arguman project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from datetime import timedelta

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qlp_henm3k-$7u@9b(@coqgpd1-2xmtox%a8_#*r9=0wh5d0oo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'typogrify',
    'social_auth',
    'django_gravatar',
    'rest_framework',
    'rest_framework.authtoken',
    'profiles',
    'premises',
    'nouns',
    'newsfeed',
    'blog',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'i18n.middleware.SubdomainLanguageMiddleware',
    'i18n.middleware.MultipleProxyMiddleware'
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "redis_cache.cache.RedisCache",
#         "LOCATION": "127.0.0.1:6379:1"
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

PREVENT_LANGUAGE_REDIRECTION = False

REDIRECTED_PATHS = (
    '/',
    '/newsfeed',
    '/news',
    '/stats',
    '/about',
    '/blog',
    '/new-argument'
)

DEFAULT_LANGUAGE = 'en'

BASE_DOMAIN = 'arguman.org'

AVAILABLE_LANGUAGES = (
    'tr',
    'en',
    'ch'
)

LANGUAGE_CODE_MAPPING = {
    'ch': 'zh-Hans'
}

LANGUAGE_CODE_MAPPING_REVERSED = {
    v.lower(): k for k, v in LANGUAGE_CODE_MAPPING.iteritems()
}

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "../static"),
)


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "../templates"),
)


# Social Auth Settings
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)


AUTH_USER_MODEL = 'profiles.Profile'


# Rules
CONTENT_DELETION = {
    'MAX_PREMISE_COUNT': 2,
    'HAS_EMPTY_CONTENT_DELETION': True,
    'LAST_DELETION_DATE': timedelta(hours=1)
}

TWITTER_CONSUMER_KEY = None  # defined in settings_local.py
TWITTER_CONSUMER_SECRET = None  # defined in settings_local.py

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages")

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)

DEFAULT_FROM_EMAIL = 'info@arguman.org'
EMAIL_BACKEND = 'main.postmark_backend.EmailBackend'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/hour',
        'user': '2000/hour'
    },
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'UNICODE_JSON': False,
    'DATETIME_FORMAT': '%d-%m-%Y %H:%m'
}

MONGODB_HOST = "localhost"
MONGODB_DATABASE = "arguman"

SITE_URL = "arguman.org"

# Markitup Settings
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False})

BLOG_FEED_TITLE = "Arguman.org Blog'u"
BLOG_FEED_DESCRIPTION = "Arguman analizi platformu"
BLOG_URL = "http://arguman.org/blog"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
     },
    }
}

try:
    from settings_local import *
except ImportError:
    print "settings_local.py not found!"
