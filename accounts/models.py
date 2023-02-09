from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователей"""

    def __str__(self):
        return self.username


class UsersPhones(models.Model):
    """Модель телефонов пользователей"""
    user = models.ForeignKey(CustomUser, verbose_name='User', null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField('phone', max_length=40, unique=True)

