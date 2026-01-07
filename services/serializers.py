from rest_framework import serializers
from .models import Service, ServiceFeature


class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ['id', 'name', 'order']


class ServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'icon', 'color', 'order', 'features', 'is_active', 'created_at', 'updated_at']

