from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'excerpt', 'content', 'author', 'date', 'read_time', 
                  'category', 'image', 'featured', 'slug', 'is_published', 'created_at', 'updated_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'excerpt', 'author', 'date', 'read_time', 
                  'category', 'image', 'featured', 'slug']

