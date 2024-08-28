from django.contrib import admin

from apps.gym import models

admin.site.register(models.MuscleGroups)
admin.site.register(models.Exercises)
