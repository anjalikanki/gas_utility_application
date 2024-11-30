from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions', 
        blank=True,
    )

    def _str_(self):
        return self.username


class ServiceRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('installation', 'Installation'),
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100, choices=REQUEST_TYPE_CHOICES)  
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='service_requests/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
