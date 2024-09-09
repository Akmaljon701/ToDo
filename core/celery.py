import os
from celery import Celery
import requests
from datetime import datetime
from decouple import config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def send_sms_to_telegram(self):
    from task import models, serializers

    tasks = models.Task.objects.all()
    serializer = serializers.TaskGetSerializer(tasks, many=True)

    token = config('BOT_TOKEN')
    chat_id = config('USER_ID')

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    message = f'{datetime.now()}\n\nCelery is working! \n \nData: \n{serializer.data}'
    data = {
        'chat_id': chat_id,
        'text': message
    }

    response = requests.post(url=url, params=data)

    print('Response status code:', response.status_code)
    print('Response text:', response.text)
    print('Celery is working!')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, send_sms_to_telegram.s(), name='send every 5')
