import json

import requests
from django.conf import settings
from django.db import models

from EuropeanPlumbingService.base_model import BaseModelNamedEntities
from accounts.models import Clients
from kitstructure.utils import send_request_to_api_kit_service


class AppObjet(BaseModelNamedEntities):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    db_name = models.CharField(null=True, max_length=255)
    comment = models.TextField(null=True)

    def _generate_data_for_service(self):
        return {
            "client_id": self.client_id,
            "api_id": self.id,
            "db_name": f'{self.db_name}_{self.id}',
            "user": "user",
            "password": "password",
        }

    def generate_data_for_crete_db(self):
        """отправляет запрос в сервис для создания ДБ и записи о ней"""
        payload = self._generate_data_for_service()
        print('payload', payload)
        response = send_request_to_api_kit_service(uri=f'clientdb', data=payload, method='POST')
        return response.status_code == 200

    def delete(self, using=None, keep_parents=False):
        response = send_request_to_api_kit_service(uri=f'clientdb/by/appid/{self.id}', method='DELETE')
        if response.status_code == 200:
            return super().delete(using=None, keep_parents=False)
        raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')


    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        response = self.change_data()
        if response.status_code == 200:
            raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')
        return super()._do_update(base_qs, using, pk_val, values, update_fields, forced_update)

    def change_data(self):
        payload = self._generate_data_for_service()
        print('payload update', payload)
        response = send_request_to_api_kit_service(uri=f'clientdb', data=payload, method='PUT')
        return response

class TagsForApi(BaseModelNamedEntities):
    """"""
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)


class Entities(BaseModelNamedEntities):
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)
    structure = models.JSONField('структура данных')
    table_name = models.CharField('название таблицы в БД', max_length=120)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        response = send_request_to_api_kit_service(uri=f'table/create/{self.app_id}/{self.table_name}',
                                                   data=json.loads(self.structure), method='POST')
        if response.status_code == 200:
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')

    def delete(self, using=None, keep_parents=False):
        response = send_request_to_api_kit_service(uri=f'table/create/{self.app_id}/{self.table_name}', method='DELETE')
        if response.status_code == 200:
            return super().delete(using=None, keep_parents=False)
        raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')


class ApiOfApp(BaseModelNamedEntities):
    app = models.ForeignKey(AppObjet, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagsForApi, null=True)
    entities = models.ForeignKey(Entities, null=True, on_delete=models.CASCADE)
    prefix = models.CharField('префикс в url', max_length=50)

    def save_row_to_api(self, data):
        response = send_request_to_api_kit_service(uri=f'table/insert/{self.app_id}/{self.entities.table_name}',
                                                   method='POST', data=data)
        if response.status_code == 200:
            return response.json()
        raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')

    def get_rows_from_api(self, limit: int = 10, offset: int = 0):
        response = send_request_to_api_kit_service(uri=f'table/{self.app_id}/{self.entities.table_name}?limit={limit}&offset={offset}',
                                                   method='GET')
        if response.status_code == 200:
            return response.json()
        raise ValueError(f'Ошибка доcтупа к сервису -> {response.text}')