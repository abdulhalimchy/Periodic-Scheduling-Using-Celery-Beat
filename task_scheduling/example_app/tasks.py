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