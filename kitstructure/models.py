import requests
from django.conf import settings
from django.db import models

from EuropeanPlumbingService.base_model import BaseModelNamedEntities
from accounts.models import Clients
from kitstructure.utils import send_request_to_api_kit_service


class AppObjet(BaseModelNamedEntities):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def generate_data_for_crete_db(self):
        """отправляет запрос в сервис для создания ДБ и записи о ней"""
        payload = {
            "client_id": self.client_id,
            "api_id": self.id,
            "db_name": f'{self.name}_{self.id}',
            "user": "user",
            "password": "password",
        }
        print('payload', payload)
        response = send_request_to_api_kit_service(uri=f'clientdb', data=payload, method='POST')
        return response.status_code == 200

    def delete(self, using=None, keep_parents=False):
        response = send_request_to_api_kit_service(uri=f'clientdb/by/appid/{self.id}', method='DELETE')
        if response.status_code == 200:
            return super().delete(using=None, keep_parents=False)
        raise ValueError('Ошибка доcтупа к сервису')


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
