from django import forms

from apps.core.forms import BaseForm
from apps.gym.forms import CreateWorkoutForm
from apps.organizations import models


class RegisterEmployeeForm(BaseForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    document = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    role = forms.ChoiceField(
        choices=models.GymEmployee.Roles.choices,
        required=True,
    )


class ProfessorCreateWorkoutForm(CreateWorkoutForm):
    student = forms.ModelChoiceField(
        queryset=models.Users.objects.all(),
        required=True,
    )
