from django.contrib import admin
from .models import Experience, ExperienceAchievement


class ExperienceAchievementInline(admin.TabularInline):
    model = ExperienceAchievement
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'period_start', 'period_end', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'company', 'description']
    inlines = [ExperienceAchievementInline]
    ordering = ['-order']


@admin.register(ExperienceAchievement)
class ExperienceAchievementAdmin(admin.ModelAdmin):
    list_display = ['text', 'experience', 'order']
    list_filter = ['experience']
    search_fields = ['text', 'experience__title']
    ordering = ['experience', 'order']
