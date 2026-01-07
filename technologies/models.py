from django.db import models


class Technology(models.Model):
    CATEGORY_CHOICES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('CMS', 'CMS'),
        ('Website Builder', 'Website Builder'),
        ('Static Sites', 'Static Sites'),
        ('Cloud', 'Cloud'),
        ('Database', 'Database'),
        ('DevOps', 'DevOps'),
        ('CI/CD', 'CI/CD'),
        ('Marketing', 'Marketing'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Technologies'
    
    def __str__(self):
        return f"{self.name} ({self.category})"
