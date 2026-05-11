from django.db import models

from apps import members
from apps import pastors
from apps import services
# Create your models here.

import uuid

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey("members.Member", on_delete=models.DO_NOTHING)
    service = models.ForeignKey("services.Service", on_delete=models.DO_NOTHING, null=True, blank=True)
    service_type = models.CharField(max_length=32)
    service_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'
        managed = False
