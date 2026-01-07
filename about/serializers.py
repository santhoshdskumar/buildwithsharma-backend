from rest_framework import serializers
from .models import AboutContent, AboutHighlight


class AboutHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHighlight
        fields = ['id', 'title', 'description', 'icon', 'order', 'is_active']


class AboutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContent
        fields = ['id', 'section_title', 'description', 'order', 'is_active', 'created_at', 'updated_at']

