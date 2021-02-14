# Periodic Task using Celery-beat

This repository is containing a basic example project about periodic task using celery-beat. I used RabbitMQ as message broker.

## Install all dependencies

    cd to the directory where requirements.txt is located
    activate your virtualenv
    run: pip install -r requirements.txt in your shell

## Setup Celery Settings
Create a file **celery.py** in project folder. In this example, task_scheduling/task_scheduling/**celery.py**
```python
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_scheduling.settings')

app = Celery('task_scheduling')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```
Now, in task_scheduling/task_scheduling/**settings.py** add the following settings:
```python
# Celery related settings
CELERY_BROKER_URL='amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

## Periodic Task
For periodic task, i used celery-beat. Register celery-beat in installed apps. task_scheduling/task_scheduling/**settings.py**
```python
INSTALLED_APPS = [
	.
	.
	.
    'django_celery_beat',
]
```
Now, to migrate run this command in shell/cmd:
```python
python manage.py migrate
```
Create an app and register this app in installed app in task_scheduling/task_scheduling/**settings.py**. In this project, example_app. Then create a file **tasks.py** inside this app. Then add tasks in this file. Here task_scheduling/example_app/**tasks.py** is:
```python
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from task_scheduling.celery import app

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # every minute
    sender.add_periodic_task(
        crontab(minute='*/1'),
        send_fake_email.s()
    )

    # every 10 seconds
    sender.add_periodic_task(
        10.0,
        send_notification.s()
    )



@app.task(name='send_fake_email')
def send_fake_email():
    # Code below to send email

    logger.info('Email has sent successfully')


@app.task(name='send_notification')
def send_notification():
    # Code below to send notification

    logger.info('Notification has sent successfully')
```

## Run django-server
Run the following commnad:
```
python manage.py runserver
```
## Start RabbitMQ
To enable rabbitmq management service for windows, run the following command:
```
rabbitmq-plugins enable rabbitmq_management
```
To start rabbitmq service for windows, run the following command:
```
rabbitmq-service.bat start
```
## Start Celery Worker
To start celery worker for windows, run the following command:
```
celery -A <project_name> worker -l info --pool=solo
```
## Start Celery Beat
To start celery-beat for windows, run the following command:
```
celery -A <project_name> beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```