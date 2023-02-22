from django.contrib import admin

from account.models import User
from notification.models import Post

# Register your models here.

admin.site.register(Post)
admin.site.register(User)
