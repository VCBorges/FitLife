from django.contrib import admin

from app.gym import models

admin.site.register(models.MuscleGroups)
admin.site.register(models.Equipments)
admin.site.register(models.Exercises)
