from django.db import models

from EuropeanPlumbingService.base_model import BaseModelNamedEntities
from accounts.models import Clients


class AppObjet(BaseModelNamedEntities):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)


class TagsForApi(BaseModelNamedEntities):
    """"""
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)


class Entities(BaseModelNamedEntities):
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)
    structure = models.JSONField('структура данных')
    table_name = models.CharField('название таблицы в БД', max_length=120)


class ApiOfApp(BaseModelNamedEntities):
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagsForApi, null=True)
    prefix = models.CharField('префикс в url', max_length=50)
