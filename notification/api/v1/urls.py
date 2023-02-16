from django.urls import path, include
from rest_framework.routers import DefaultRouter
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from .viewsets import (
    ScheduleNotificationViewSet, PostViewSet, LikePostViewSet,
)


router = DefaultRouter()
router.register("schedule_notification", ScheduleNotificationViewSet, basename="schedule_notification")
router.register("create_post", PostViewSet, basename='create_post')
router.register("like_post", LikePostViewSet, basename='like_post')
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/android', GCMDeviceAuthorizedViewSet)

urlpatterns = [
    path("", include(router.urls)),
]