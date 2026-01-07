from rest_framework import serializers
from .models import Experience, ExperienceAchievement


class ExperienceAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceAchievement
        fields = ['id', 'text', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    achievements = ExperienceAchievementSerializer(many=True, read_only=True)
    period = serializers.ReadOnlyField()
    
    class Meta:
        model = Experience
        fields = ['id', 'title', 'company', 'location', 'period_start', 'period_end', 
                  'period', 'description', 'achievements', 'order', 'is_active', 
                  'created_at', 'updated_at']

