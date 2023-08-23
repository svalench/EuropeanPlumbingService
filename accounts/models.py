from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt
from rest_framework.authtoken.models import Token
from django.conf import settings


class BaseClassModel(models.Model):
    """базовый класс для создания моделей"""
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    """Модель пользователей"""
    client = models.ForeignKey('Clients', verbose_name='client', null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey('UsersRoles', verbose_name='role', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.username


class CustomToken(Token):

    def generate_key(self) -> str:
        encoded_jwt = jwt.encode({"id": self.user.pk}, settings.SECRET_JWT, algorithm="HS256")
        return encoded_jwt

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True


class UsersPhones(BaseClassModel):
    """Модель телефонов пользователей"""
    user = models.ForeignKey(CustomUser, verbose_name='User', null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField('phone', max_length=40, unique=True)

    def __str__(self):
        return self.phone


class Clients(BaseClassModel):
    """модель клиентов (сущность которая определяет именно клиента в рамках проекта,
     у него может быть несколько юр лиц или организаций)
     """
    admin = models.ForeignKey(CustomUser, verbose_name='Admin', on_delete=models.DO_NOTHING)
    name = models.CharField('Client name', max_length=510, unique=True)
    users = models.ManyToManyField(CustomUser, verbose_name='users', related_name='teammate')

    def __str__(self):
        return self.name


class UsersRoles(BaseClassModel):
    """
    Каталог должностей клиентов
    """
    name = models.CharField('role name', max_length=510, unique=True)
    client = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

