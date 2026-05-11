from django.db import models

from apps import members
from apps import pastors
# Create your models here.

class ConnectGroup(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    meeting_day = models.CharField(max_length=20)
    meeting_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class ConnectGroupMember(models.Model):
    connect_group = models.ForeignKey(ConnectGroup, on_delete=models.CASCADE)
    member = models.ForeignKey("members.Member", on_delete=models.CASCADE)
    joined_at = models.DateField()
    left_at = models.DateField(null=True, blank=True)


class ConnectGroupPastor(models.Model):
    connect_group = models.ForeignKey(ConnectGroup, on_delete=models.CASCADE)
    pastor = models.ForeignKey("pastors.Pastor", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)