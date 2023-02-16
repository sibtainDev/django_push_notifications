from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("account.api.v1.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]