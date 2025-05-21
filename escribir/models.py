from django.db import models

# This app doesn't store data locally, it forwards to the database service
# So we just define a simple placeholder model for Django requirements

class WriteOperation(models.Model):
    operation_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'write_operations'