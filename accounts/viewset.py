from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.models import CustomUser
from accounts.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer