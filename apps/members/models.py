from pyclbr import Class
from venv import create

from django.db import models
from djangoyearlessdate.models import YearlessDateField

# Create your models here.

import uuid

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=32, null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'members'  # This points Django to your existing table
        managed = False       # This tells Django not to try and change this table


class FirstTimers(models.Model):

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    service_id = models.ForeignKey("services.Service", null=True, blank=True, on_delete=models.SET_NULL)
    service_name = models.CharField(max_length=200)
    service_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

