# status/models.py
from django.conf import settings
from django.db import models

class Service(models.Model):
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services',
          null=True,        # allow existing rows to be null
        blank=True
    )
    STATUS_CHOICES = [
        ('OPERATIONAL', 'Operational'),
        ('DEGRADED', 'Degraded Performance'),
        ('PARTIAL_OUTAGE', 'Partial Outage'),
        ('MAJOR_OUTAGE', 'Major Outage'),
    ]

    name       = models.CharField(max_length=100)
    status     = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPERATIONAL'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

class Incident(models.Model):
    service     = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='incidents')
    title       = models.CharField(max_length=255)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Maintenance(models.Model):
    service         = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='maintenances')
    title           = models.CharField(max_length=255)
    description     = models.TextField()
    scheduled_start = models.DateTimeField()
    scheduled_end   = models.DateTimeField()
    is_completed    = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
