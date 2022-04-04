import os
from celery import Celery

from mailing import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     'mailing_task': {
#         'task': 'main.tasks.mailing_task',
#         'schedule': crontab(minute='*/1'),
#         # 'args': (),
#     }
# }


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
