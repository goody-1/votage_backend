from django.db import models

from apps import members
from apps import pastors
from apps import services
# Create your models here.

class Event(models.Model):
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class EventParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    participant_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
