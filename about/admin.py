from django.contrib import admin
from .models import AboutContent, AboutHighlight


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'order', 'is_active']
    list_filter = ['is_active']
    ordering = ['order']


@admin.register(AboutHighlight)
class AboutHighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active', 'icon']
    ordering = ['order']
