from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser
from accounts.serializer import UserSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserAuthToken(ObtainAuthToken):
    """метод для авторизации пользователя на сайте"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = now()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_admin': user.is_superuser,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

class UserAuthTokenUpdate(ObtainAuthToken):
    """метод для обновления токена на сайте"""

    def post(self, request, *args, **kwargs):
        t = Token.objects.get(user=request.user)
        t.key = t.generate_key()
        t.save()
        return Response({
            'token': t.key,
            'user_id': request.user.pk,
            'is_admin': request.user.is_superuser,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })

# class ForgotPasswordUser(viewsets.ViewSet):
#     """метод если пользователь забыл пароль то отправляем письмо с новым"""
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer
#
#     def retrieve(self, request, name=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, username=name)
#         if user.is_superuser:
#             raise PermissionDenied('Суперпользователю запрещено менять пароль')
#         new_pass = generate_new_password()
#         email = EmailSending()
#         email.send_email_forgot_password(user=user, password=new_pass)
#         return Response({"detail": "Проверьте почту. Там новый пароль."})


# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     Контроллер для смены пароля пользователя
#     """
#     queryset = CustomUser.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ChangePasswordSerializer
#
#     def update(self, request, *args, **kwargs):
#         if not request.user.check_password(request.data['old_password']):
#             raise ValidationError('старый пароль не совпал')
#         super(ChangePasswordView, self).update(request, *args, **kwargs)
#         return Response({"status": "OK"})
