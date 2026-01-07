from django.db import models


class AboutContent(models.Model):
    ICON_CHOICES = [
        ('Code', 'Code'),
        ('Users', 'Users'),
        ('Award', 'Award'),
        ('Target', 'Target'),
    ]
    
    section_title = models.CharField(max_length=200, default='My Story')
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'About Content'
    
    def __str__(self):
        return self.section_title


class AboutHighlight(models.Model):
    ICON_CHOICES = [
        ('Code', 'Code'),
        ('Users', 'Users'),
        ('Award', 'Award'),
        ('Target', 'Target'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
