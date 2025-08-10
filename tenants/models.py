from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Center(TenantMixin):
    """
    Center model representing a tenant in the multi-tenant system.
    Each center will have its own schema.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Default true, schema will be automatically created and synced when saved
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """
    Domain model for tenant routing.
    Links domains to tenants (Centers).
    """
    pass