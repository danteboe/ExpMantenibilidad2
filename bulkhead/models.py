# bulkhead/models.py
from django.db import models

class ServiceStatus(models.Model):
    """Model to control service availability"""
    service_name = models.CharField(max_length=50, unique=True)
    is_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service_name}: {'Enabled' if self.is_enabled else 'Disabled'}"
    
    class Meta:
        verbose_name_plural = "Service Statuses"