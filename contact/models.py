from django.db import models


class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Contact Info'
    
    def __str__(self):
        return f"Contact Info - {self.email}"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    service = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    timeline = models.CharField(max_length=100)
    message = models.TextField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.email}"
