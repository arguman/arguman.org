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
from django.utils.translation import ugettext_lazy as _

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

    'social_auth',
    'django_gravatar',
    'rest_framework',
    'rest_framework.authtoken',
    'profiles',
    'premises',
    'newsfeed',
    'blog',
    'api'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGES = (
    ('en', _('Ingilizce')),
    ('tr', _('Turkce')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'tr'

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

TWITTER_CONSUMER_KEY = None # defined in settings_local.py
TWITTER_CONSUMER_SECRET = None # defined in settings_local.py

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

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
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
}

MONGODB_HOST = "localhost"
MONGODB_DATABASE = "arguman"

SITE_URL = "arguman.org"

# Markitup Settings
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False})

BLOG_FEED_TITLE = _("Arguman.org Blog'u")
BLOG_FEED_DESCRIPTION = _("Arguman analizi platformu")
BLOG_URL = "http://arguman.org/blog"

try:
    from settings_local import *
except ImportError:
    print "settings_local.py not found!"
