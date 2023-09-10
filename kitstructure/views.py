import json

from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kitstructure.models import AppObjet, Entities, ApiOfApp


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_api(request):
    """создание апи и объектов с фронта"""
    app_id = request.data.get('appId', None)
    if not app_id:
        raise serializers.ValidationError({"app": "не передан id проекта"})
    table_name = request.data.get('tableName')
    if not table_name:
        raise serializers.ValidationError({"table_name": "не передано название"})
    entities_structure = request.data.get('entities', {})
    try:
        app = AppObjet.objects.get(pk=app_id, client__users=request.user)
    except AppObjet.DoesNotExist:
        raise serializers.ValidationError({"app": "не верная комбинация пользовать <-> приложение"})
    api_ = ApiOfApp(app=app, name=table_name)
    entiti = Entities(app=app, name=table_name, table_name=table_name, structure=json.dumps(entities_structure))
    entiti.save()
    api_.entities = entiti.id
    api_.save()
    return Response({"message": "Got some data!", "data": request.data})
