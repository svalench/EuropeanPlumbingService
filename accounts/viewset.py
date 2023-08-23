from django.utils.timezone import now
from rest_framework import viewsets, generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from accounts.models import CustomUser, Clients, UsersRoles, CustomToken
from accounts.serializer import UserSerializer, ClientSerializer, UserRoleSerializer, UserRoleViewsetSerializer, \
    RegisterSerializer
from rest_framework.response import Response


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        user = self.request.user
        return user.teammate.all()


class UsersRolesViewSet(viewsets.ModelViewSet):
    queryset = UsersRoles.objects.all()
    serializer_class = UserRoleViewsetSerializer


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
        token, created = CustomToken.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_admin': user.is_superuser,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'client_id': [i.id for i in user.clients_set.all()],
            'email': user.email
        })


class UserAuthTokenUpdate(ObtainAuthToken):
    """метод для обновления токена на сайте"""

    def post(self, request, *args, **kwargs):
        t = CustomToken.objects.get(user=request.user)
        t.key = t.generate_key(request.user)
        t.save()
        return Response({
            'token': t.key,
            'user_id': request.user.pk,
            'is_admin': request.user.is_superuser,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })


class RegisterView(generics.CreateAPIView):
    """контроллер регистрации нового пользователя"""
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = CustomUser.objects.get(username=serializer.data['username'])
        data.is_active = True
        data.save()
        # email = EmailSending()
        # data1 = {"newpassword": request.data.get('password'), "name": data.first_name, "last_name": data.last_name}
        # email.send_mail(email=data.email, subject='Регистрация на Arhiterm', template='email_template/email_change_pass.html',data=data1)
        return Response({"id": data.id, "username": data.username}, status=status.HTTP_201_CREATED, headers=headers)

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
