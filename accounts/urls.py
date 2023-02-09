from django.urls import path

from accounts.views import get_me

urlpatterns = [
    path('me/', get_me),
]