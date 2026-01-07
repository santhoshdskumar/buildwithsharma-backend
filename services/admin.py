from django.contrib import admin
from .models import Service, ServiceFeature


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'color', 'order', 'is_active']
    list_filter = ['is_active', 'color']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'order']
    list_filter = ['service']
    search_fields = ['name', 'service__title']
    ordering = ['service', 'order']
