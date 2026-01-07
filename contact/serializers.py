from rest_framework import serializers
from .models import ContactInfo, ContactSubmission


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'email', 'phone', 'location', 'is_active']


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'company', 'service', 'budget', 'timeline', 'message']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user_agent = ''
        referrer = ''
        ip_address = None
        
        if request:
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referrer = request.META.get('HTTP_REFERER', '')
            ip_address = self.get_client_ip(request)
        
        submission = ContactSubmission.objects.create(
            **validated_data,
            user_agent=user_agent,
            referrer=referrer,
            ip_address=ip_address
        )
        return submission
    
    def get_client_ip(self, request):
        if not request:
            return None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

