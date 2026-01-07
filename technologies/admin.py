from django.contrib import admin
from .models import Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name']
    ordering = ['order', 'name']
