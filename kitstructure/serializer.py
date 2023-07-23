import uuid

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from accounts.serializer import ClientSerializer
from accounts.utils import check_email
from kitstructure.models import AppObjet, ApiOfApp, TagsForApi, Entities


class AppObjetSerializer(serializers.ModelSerializer):
    #client = ClientSerializer()

    def create(self, validated_data):
        app = AppObjet.objects.create(
            **validated_data
        )
        app.save()
        if not app.generate_data_for_crete_db():
            app.delete()
            raise ValidationError(detail='не доступен сервис API KIT', code=400)
        return app


    class Meta:
        model = AppObjet
        fields = '__all__'


class TagsForApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsForApi
        fields = '__all__'


class ApiOfAppSerializer(serializers.ModelSerializer):
    app = AppObjetSerializer()
    tags = TagsForApiSerializer(many=True, read_only=True)

    class Meta:
        model = ApiOfApp
        fields = '__all__'


class EntitiesSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Entities
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if not check_email(attrs['username']):
            raise serializers.ValidationError({"username": "Не верный формат email адреса"})
        return attrs

    def create(self, validated_data):
        entities = Entities.objects.create(
            name=validated_data['name'],
            structure=validated_data['structure'],
            app=validated_data['app'],
            table_name=uuid.uuid4(),
        )
        entities.save()
        return entities
