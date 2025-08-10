from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from tenants.models import Center

class User(AbstractUser):
    """
    Custom User model that will be stored in the public schema.
    Users can be associated with centers but exist globally.
    """
    email = models.EmailField(unique=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_center_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # <-- Çakışmayı önler
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",  # <-- Çakışmayı önler
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} - {self.center.name if self.center else 'No Center'}"
