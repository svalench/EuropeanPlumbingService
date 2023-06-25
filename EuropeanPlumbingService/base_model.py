from django.db import models


class BaseDjangoModel(models.Model):
    """Базовая модель для сущностей"""
    created_at = models.DateTimeField('Время последнего обновления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата создания', auto_now=True)

    class Meta:
        abstract = True


class BaseModelNamedEntities(BaseDjangoModel):
    name = models.CharField('Название', null=False, db_index=True, max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
