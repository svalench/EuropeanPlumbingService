from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователей"""
    client = models.ForeignKey('Clients', verbose_name='client', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class UsersPhones(models.Model):
    """Модель телефонов пользователей"""
    user = models.ForeignKey(CustomUser, verbose_name='User', null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField('phone', max_length=40, unique=True)

    def __str__(self):
        return self.phone


class Clients(models.Model):
    admin = models.ForeignKey(CustomUser, verbose_name='Admin', on_delete=models.CASCADE)
    name = models.CharField('Client name', max_length=510, unique=True)
