from django.contrib import admin

from apps.gym import models

admin.site.register(models.MuscleGroup)
admin.site.register(models.Exercise)
