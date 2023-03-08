from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    username = models.CharField("Username", max_length=35, unique=True, null=True, blank=True)
    last_login = None
    phone = models.CharField("Phone Number", max_length=15, null=True, blank=True)
    is_notification_on = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


"""
AbstractBaseUser basically provide only 3 fields id, password and last_login, So i am using this one
AbstractUser provide 11 all fields and you can add extra fields 
"""
