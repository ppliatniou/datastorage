import os

DEBUG = True

STATIC_ROOT = "/www/app/static/"

if not os.environ.get("SKIP_INIT", False):
    DATABASES = {
        'default': {
            'HOST': os.environ['DATABASE_DEFAULT_HOST'],
            'NAME': os.environ['DATABASE_DEFAULT_NAME'],
            'ENGINE': 'django.db.backends.postgresql',
            'USER': os.environ['DATABASE_DEFAULT_USER'],
            'PASSWORD': os.environ['DATABASE_DEFAULT_PASSWORD'],
            'PORT': int(os.environ['DATABASE_DEFAULT_PORT'])
        }
    }
    
    STATIC_URL = os.environ['STATIC_URL']
    
    # Celery application definition
    CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

