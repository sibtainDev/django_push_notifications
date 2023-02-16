from celery import shared_task
from celery.utils.log import get_task_logger


from .models import Notification

logger = get_task_logger(__name__)


@shared_task()
def send_schedule_notifications(*args, **kwargs):
    logger.info("send_schedule_notification")
    Notification.objects.create(sender_id=kwargs['sender'], title=kwargs['title'],
                                message=kwargs['message'])


