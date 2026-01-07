from django.contrib import admin
from .models import ContactInfo, ContactSubmission


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'location', 'is_active']
    list_filter = ['is_active']


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'is_read', 'created_at']
    list_filter = ['is_read', 'service', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'user_agent', 'referrer', 'ip_address']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
