from django.db import models

from hostel.models import Hostel


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT, related_name="students")
    external_id = models.CharField(max_length=64)
    full_name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    room_number = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["hostel", "external_id"], name="unique_student_external_id_per_hostel")]
        indexes = [models.Index(fields=["hostel", "status", "full_name"])]
        ordering = ["full_name"]


class RosterImport(models.Model):
    class Status(models.TextChoices):
        PREVIEWED = "previewed", "Previewed"
        COMMITTED = "committed", "Committed"
        FAILED = "failed", "Failed"

    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT)
    digest = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PREVIEWED)
    accepted_rows = models.PositiveIntegerField(default=0)
    rejected_rows = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["hostel", "digest"], name="unique_roster_digest_per_hostel")]
