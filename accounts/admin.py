from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UsersPhones


class UsersPhonesAdmin(admin.StackedInline):
    list_display = ["id", "phone",]
    model = UsersPhones


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [UsersPhonesAdmin]
    list_display = ["id", "email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)


