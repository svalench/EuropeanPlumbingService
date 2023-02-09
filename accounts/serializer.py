from rest_framework import serializers

from accounts.models import CustomUser, UsersPhones


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersPhones
        exclude = ('user',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    phones = UserPhoneSerializer(read_only=True, many=True, source='usersphones_set.all')
    class Meta:
        model = CustomUser
        exclude = ('password',)
