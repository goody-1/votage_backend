from django.db import models

from django.core.exceptions import ValidationError

# Create your models here.
import apps.members.models as members_models
from apps import members
from apps import pastors
from apps import services


class Directorate(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    director = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directorates_led"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    directorate = models.ForeignKey(
        Directorate,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    hod = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments_led"
    )

    assistant_hod = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments_assisted"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def unit_heads(self):
        """Returns all current unit heads under this department"""
        return members_models.Member.objects.filter(
            units_led__department=self,
            units_led__unit_head__isnull=False
        ).distinct()

    def get_all_members(self):
        """All people in this department — either directly or via units"""
        from django.db.models import Q

        direct = members_models.Member.objects.filter(
            departmentmembership__department=self,
            departmentmembership__is_active=True
        )

        via_units = members_models.Member.objects.filter(
            unit_membership__unit__department=self,
            unit_membership__is_active=True
        )

        return (direct | via_units).distinct()




class DepartmentMembership(models.Model):
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    joined_at = models.DateField()

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "department"],
                name="unique_member_department"
            )
        ]
        indexes = [
            models.Index(fields=["member"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return f"{self.member} - {self.department}"
    

class Unit(models.Model):
    """
    Sub-division / Unit inside a Department.
    Example: Media department → Live Streaming, Camera, Graphics, etc.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="units"
    )

    # Unit-level leader (often called Assistant HOD, Coordinator, Unit Head, etc.)
    unit_head = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="units_led",
        verbose_name="Unit Head / Assistant HOD"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("name", "department")]   # Prevent duplicate unit names in same dept
        ordering = ["name"]
        indexes = [
            models.Index(fields=["department"]),
            models.Index(fields=["unit_head"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.department.name})"

    def clean(self):
        # Optional: you can add validation if needed
        if self.unit_head and not self.department.hod:
            # Some churches require department HOD before unit leaders
            pass  # or raise ValidationError if you want to enforce it

    def save(self, *args, **kwargs):
        self.full_clean()  # runs clean() if you added validation
        super().save(*args, **kwargs)

    @property
    def hod(self):
        """The department HOD — shared across all units in the dept"""
        return self.department.hod


class UnitMembership(models.Model):
    """
    Many-to-many link between Member ↔ Unit
    (similar to DepartmentMembership)
    """
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="unit_memberships"
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    joined_at = models.DateField(auto_now_add=False)  # or DateTimeField if you want time
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Camera Operator, Graphics Designer, Stream Technician..."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "unit"],
                name="unique_member_unit"
            )
        ]
        indexes = [
            models.Index(fields=["member"]),
            models.Index(fields=["unit"]),
        ]

    def __str__(self):
        return f"{self.member} — {self.unit}"
