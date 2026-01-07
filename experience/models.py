from django.db import models


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    period_start = models.CharField(max_length=50)
    period_end = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def period(self):
        if self.period_end:
            return f"{self.period_start} - {self.period_end}"
        return f"{self.period_start} - Present"


class ExperienceAchievement(models.Model):
    experience = models.ForeignKey(Experience, related_name='achievements', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.experience.title} - {self.text[:50]}"
