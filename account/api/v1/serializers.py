from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User
from utils.helper import check_email

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        user = User(
            username=validated_data.get('email').split('@')[0],
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
        user_name = attrs.get("email")
        password = attrs.get("password")

        if check_email(user_name) is False:
            try:
                user = User.objects.get(Q(username=user_name) | Q(phone=user_name))
                if user.check_password(password):
                    attrs['email'] = user.email

                """
                 In my case, I used the Email address as the default Username 
                 field in my custom User model. so that I get the user email 
                 from the Users model and set it to the attrs field. You can 
                 be modified as your setting and your requirement 
                """

            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    'No such user with provided credentials'.title())

        data = super().validate(attrs)
        return data

