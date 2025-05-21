from django.db import models

class ServiceStatus(models.Model):
    service_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service_name} - {'Active' if self.is_active else 'Inactive'}"
    
    class Meta:
        db_table = 'service_status'