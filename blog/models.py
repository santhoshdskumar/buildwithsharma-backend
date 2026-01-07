from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    content = models.TextField(blank=True)
    author = models.CharField(max_length=100, default='BuildWithSharma')
    date = models.DateField()
    read_time = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    image = models.URLField(max_length=500, blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=300)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return self.title
