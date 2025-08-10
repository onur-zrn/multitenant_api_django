from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Sample(models.Model):
    """
    Sample model that will be stored in each tenant's schema.
    Each center will have its own samples isolated from other centers.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    sample_type = models.CharField(max_length=100)
    collection_date = models.DateTimeField()
    processed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('collected', 'Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='collected')
    
    # Metadata fields
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.CharField(max_length=150)  # Store user email/username since User is in public schema
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.status}"

class SampleResult(models.Model):
    """
    Results associated with samples in tenant schema.
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='results')
    test_name = models.CharField(max_length=200)
    result_value = models.TextField()
    unit = models.CharField(max_length=50, blank=True, null=True)
    reference_range = models.CharField(max_length=100, blank=True, null=True)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sample.name} - {self.test_name}: {self.result_value}"