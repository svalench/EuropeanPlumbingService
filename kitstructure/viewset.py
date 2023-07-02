from django.utils.timezone import now
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from kitstructure.models import AppObjet, ApiOfApp, Entities
from kitstructure.serializer import AppObjetSerializer, ApiOfAppSerializer, EntitiesSerializer


class AppObjetSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AppObjet.objects.all()
    serializer_class = AppObjetSerializer

    def get_queryset(self):
        user = self.request.user
        return AppObjet.objects.filter(client__users=user).prefetch_related('client__users').select_related('client')


class ApiOfAppViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ApiOfApp.objects.all()
    serializer_class = ApiOfAppSerializer

    def get_queryset(self):
        user = self.request.user
        return ApiOfApp.objects.filter(app__client__users=user).select_related('app', 'app__client').prefetch_related('tags')


class EntitiesSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Entities.objects.all()
    serializer_class = EntitiesSerializer

