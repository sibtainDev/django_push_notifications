import json

from django.db.models import Q
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from notification.api.v1.serializers import ScheduleNotificationSerializer, PostSerializer, LikePostSerializer
from notification.models import Notification, AdminPeriodTask, Post, LikePost
from utils.helper import generate_random_name, add_notifications


class ScheduleNotificationViewSet(ModelViewSet):
    """
        This api will use for scheduling notification, a user will add message and time at which
         notification will be sent. Then we will create schedule task.
         'AdminPeriodTask' is store history, this will be used when a user update notification time,
         the previous periodic task of same id of notification and periodic_task will be deleted.


    """
    serializer_class = ScheduleNotificationSerializer
    queryset = Notification.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(Q(receiver=self.request.user) | Q(receiver__isnull=True))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        task_time = ClockedSchedule.objects.create(clocked_time=obj.schedule_notification_time)
        name = obj.title
        if PeriodicTask.objects.filter(name=name).exists():
            # periodic_task name unique field so it will generate a random name if a name already exist
            name = generate_random_name(obj.title)
        period = PeriodicTask.objects.create(
            clocked=task_time,
            name=name,
            task='home.tasks.send_schedule_notification',
            one_off=True,
            kwargs=json.dumps({
                'title': obj.title,
                'message': obj.message,
                'sender': obj.sender.id,
            })
        )
        AdminPeriodTask.objects.create(notify=obj, period=period)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
            on update it will first delete the previous Periodic Task and create new one
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        task_ids = AdminPeriodTask.objects.filter(notify=instance)
        PeriodicTask.objects.filter(id__in=task_ids.values('period_task__id'),
                                    clocked__clocked_time=instance.schedule_notification_time).delete()
        if task_ids.exists():
            task_ids.delete()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        name = obj.title
        if PeriodicTask.objects.filter(name=name).exists():
            name = generate_random_name(obj.title)
        task_time = ClockedSchedule.objects.create(clocked_time=obj.schedule_notification_time)
        PeriodicTask.objects.create(
            clocked=task_time,
            name=name,
            task='home.tasks.send_schedule_notification',
            one_off=True,
            kwargs=json.dumps({
                'title': obj.title,
                'message': obj.message,
                'sender': obj.sender.id,
            })
        )
        return Response(serializer.data)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]


class LikePostViewSet(ModelViewSet):
    serializer_class = LikePostSerializer
    queryset = LikePost.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        user = self.request.user
        if post_id is not None:
            post_query = LikePost.objects.filter(user=user, post__id=post_id, is_like=True)
            if post_query.exists():
                post_query.delete()
                return Response("UnLike", status=status.HTTP_200_OK)
            LikePost.objects.create(user=user, post_id=post_id, is_like=True)
            post = Post.objects.get(id=post_id)
            message = f"{user.username} liked your post"
            add_notifications(title="Post Like", message=message, sender=user, receiver=post.created_by)
            return Response("Liked", status=status.HTTP_200_OK)
        return Response("post_id required")
