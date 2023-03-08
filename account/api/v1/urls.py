from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.api.v1.viewsets import UserRegistrationView, LoginTokenObtainView, AllUserDataView, UpdateUserView

router = routers.SimpleRouter()
router.register("all_user_data", AllUserDataView, basename="all_user_data")
router.register("update_user", UpdateUserView, basename="update_user")

urlpatterns = [

    path('', include(router.urls)),
    path('signup/', UserRegistrationView.as_view(), name="signup"),
    path('login/', LoginTokenObtainView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
