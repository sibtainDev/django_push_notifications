from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from account.models import User


# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_notification", null=True,
                               blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_receiver", null=True,
                                 blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    schedule_notification_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)


class AdminPeriodTask(models.Model):
    notify = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notify_history')
    period = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, related_name='periodic_history')


class Post(models.Model):
    post_title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='post', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_owner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_title} >> {self.created_by}"


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post}  >> {self.user}"


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    from push_notifications.models import APNSDevice, GCMDevice
    if created:
        if instance.receiver:
            devices = GCMDevice.objects.filter(user_id=instance.receiver, user_id__is_notification_on=True)
            apns_devices = APNSDevice.objects.filter(user_id=instance.receiver, user_id__is_notification_on=True)
        else:
            devices = GCMDevice.objects.filter(user_id__is_notification_on=True)
            apns_devices = APNSDevice.objects.filter(user_id__is_notification_on=True)

        if devices or apns_devices:
            try:
                devices.send_message(title=instance.title, message=instance.message)
                apns_devices.send_message(message={"body": instance.message})
                print("===============================message send")
            except Exception as e:
                print('===================', e)
