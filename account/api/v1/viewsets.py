from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from account.api.v1.serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer, AllUserSerializer
from account.models import User


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class AllUserDataView(ModelViewSet):
    serializer_class = AllUserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


class UpdateUserView(ModelViewSet):
    serializer_class = AllUserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

