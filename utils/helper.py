from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask

from notification.models import Notification


def check_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def generate_random_name(text):
    import random
    new_text = f"{text}{random.randint(0, 10)}"
    if PeriodicTask.objects.filter(name=new_text).exists():
        return generate_random_name(new_text)
    else:
        return new_text

def add_notifications(title, message, sender, receiver=None):
    notify = Notification()
    notify.sender = sender
    notify.title = title
    notify.message = message
    if receiver:
        notify.receiver = receiver
    notify.save()
