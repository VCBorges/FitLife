from django.contrib import admin

from ..users.models import Users

# Register your models here.

# register user model
admin.site.register(Users)
