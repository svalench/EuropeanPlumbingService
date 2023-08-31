from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser, UsersPhones, Clients, UsersRoles
from accounts.utils import check_email


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersPhones
        exclude = ('user',)


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRoles
        exclude = ('client',)


class UserRoleViewsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRoles
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    phones = UserPhoneSerializer(read_only=True, many=True, source='usersphones_set.all')
    role = UserRoleSerializer(read_only=True)

    class Meta:
        model = CustomUser
        exclude = ('password',)


class RegisterSerializer(serializers.ModelSerializer):
    """класс сериализованной модели регистрации пользователя"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if not check_email(attrs['username']):
            raise serializers.ValidationError({"username": "Не верный формат email адреса"})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            is_active=False
        )
        # email = EmailSending()
        # email.send_email_registration(user=user)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'



class ChangePasswordSerializer(serializers.ModelSerializer):
    """Класс предназначен для обновления пароля пользователя
    Вводится новый  пароль password  подтверждение пароля password2  и старый пароль old_password
    """
    # password = serializers.CharField(write_only=True, required=True, validators=[validators.validate_password])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Указанные пароли не совпадают."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Неверно введен старый пароль"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
