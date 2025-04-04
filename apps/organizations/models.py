from django.db import models

from apps.core.models import BaseModel
from apps.users.models import Users


class Gym(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='owned_gyms',
    )
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    students = models.ManyToManyField(
        Users,
        related_name='student_gyms',
        blank=True,
    )

    class Meta:
        db_table = 'gyms'
        verbose_name = 'Gym'
        verbose_name_plural = 'Gyms'
        default_related_name = 'gyms'


class GymEmployee(BaseModel):
    class Roles(models.TextChoices):
        OWNER = 'owner'
        PROFESSOR = 'professor'

    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, related_name='instructors')
    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.PROFESSOR,
    )
    joined_at = models.DateTimeField()

    class Meta:
        db_table = 'gym_employees'
        verbose_name = 'Gym Employee'
        verbose_name_plural = 'Gym Employees'
        default_related_name = 'gym_employees'


class GymStudentProfile(BaseModel):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    gyms = models.ManyToManyField(Gym, related_name='students')
    joined_at = models.DateTimeField()

    class Meta:
        db_table = 'gym_student_profiles'
        verbose_name = 'Gym Student Profile'
        verbose_name_plural = 'Gym Student Profiles'
        default_related_name = 'gym_student_profiles'
