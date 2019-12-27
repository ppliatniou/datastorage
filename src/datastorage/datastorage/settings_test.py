from .settings import *

CELERY_TASK_ALWAYS_EAGER = True
CELERY_RESULT_BACKEND = 'file:///tmp/'

