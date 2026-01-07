from django.db import models


class Service(models.Model):
    COLOR_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('accent', 'Accent'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    
    ICON_CHOICES = [
        ('Code', 'Code'),
        ('Smartphone', 'Smartphone'),
        ('Globe', 'Globe'),
        ('Database', 'Database'),
        ('Cloud', 'Cloud'),
        ('GitBranch', 'GitBranch'),
        ('Shield', 'Shield'),
        ('Zap', 'Zap'),
        ('Mail', 'Mail'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.service.title} - {self.name}"
