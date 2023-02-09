from rest_framework import serializers

from accounts.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password',)
