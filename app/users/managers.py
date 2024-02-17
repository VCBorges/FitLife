from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import Users


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields) -> Users:
        if not email:
            raise ValidationError(_('The Email must be set'))
        email = self.normalize_email(email)
        user: Users = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> Users:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
