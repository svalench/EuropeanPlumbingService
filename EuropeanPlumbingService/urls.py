
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


from accounts.viewset import UserViewSet, UserAuthToken, ClientsViewSet, UsersRolesViewSet, RegisterView, \
    ChangePasswordView, ForgotPasswordUser
from kitstructure.views import create_api, create_new_row_in_api, get_rows_in_api
from kitstructure.viewset import AppObjetSet, ApiOfAppViewSet
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users-role', UsersRolesViewSet)
router.register(r'clients', ClientsViewSet)
router.register(r'apps', AppObjetSet)
router.register(r'apis', ApiOfAppViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/oauth/', UserAuthToken.as_view(), name='signin'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('create/api/', create_api, name='create_api'),
    path('create/item/', create_new_row_in_api, name='create_new_row_in_api'),
    path('get/item/', get_rows_in_api, name='get_rows_in_api'),
    path('user/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('change_password/backend/change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('registration/backend/forgot/password/<str:name>/', ForgotPasswordUser.as_view({'get': 'retrieve'}),
         name='forgot_password'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
