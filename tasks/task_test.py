from celery import Celery


# config = {'CELERY_BROKER_URL': 'redis://redis:6379/0',
#           'CELERY_RESULT_BACKEND': 'redis://redis:6379/0'}
config = {'CELERY_BROKER_URL': 'redis://localhost:6379/0',
          'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0'}

celery = Celery('task_test', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)


@celery.task
def is_celery_working():
    return 'celery is working!'


@celery.task
def multiple(a, b):
    return a * b



