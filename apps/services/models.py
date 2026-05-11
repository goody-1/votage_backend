from django.db import models

from apps import members
from apps import pastors
from apps import connect_groups
# Create your models here.

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)


import uuid

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'service'
        managed = False
