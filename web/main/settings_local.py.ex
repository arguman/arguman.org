DEFAULT_FROM_EMAIL = 'info@arguman.org'
POSTMARK_TOKEN = "xyz"
POSTMARK_API_URL = "https://api.postmarkapp.com/email"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
ALLOWED_HOSTS = ['*']
DEBUG = True

SERVER_EMAIL = 'info@arguman.org'
BASE_DOMAIN = 'localhost:8000' #your docker machine ip if running on virtual server
MONGODB_HOST = 'localhost' #your docker machine ip if running on virtual server

# CACHES = {
#     "default": {
#         "BACKEND": "redis_cache.cache.RedisCache",
#         "LOCATION": "127.0.0.1:6379:1"
#     }
# }
