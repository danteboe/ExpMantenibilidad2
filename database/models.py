from django.db import models
from django.utils import timezone
import uuid

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('financial', 'Financial'),
        ('technical', 'Technical'),
        ('operational', 'Operational'),
        ('strategic', 'Strategic'),
        ('compliance', 'Compliance')
    ])
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list):
        """Set tags from a list"""
        self.tags = ', '.join(tags_list)