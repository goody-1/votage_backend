from django.db import models

from apps import members
from apps import pastors
# Create your models here.

class GrowthTrack(models.Model):
    cohort_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class GrowthTrackEnrollment(models.Model):
    growth_track = models.ForeignKey(GrowthTrack, on_delete=models.CASCADE)
    member = models.ForeignKey("members.Member", on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    graduation_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["growth_track", "member"],
                name="unique_enrollment"
            )
        ]
