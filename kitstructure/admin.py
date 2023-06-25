from django.contrib import admin

from kitstructure.models import AppObjet, TagsForApi, Entities, ApiOfApp


@admin.register(AppObjet)
class AppAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'updated_at', 'created_at']
    search_fields = ['name', 'id']


@admin.register(TagsForApi)
class TagsAdmin(admin.ModelAdmin):
    list_filter = ['app']
    list_display = ['id', 'name', 'updated_at', 'created_at']
    search_fields = ['name', 'id']


@admin.register(Entities)
class EntitiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'app', 'table_name', 'updated_at', 'created_at']
    list_filter = ['app']
    search_fields = ['name', 'id', 'table_name']


@admin.register(ApiOfApp)
class ApiOfAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'prefix', 'updated_at', 'created_at']
    search_fields = ['name', 'id', 'tags', 'prefix']
