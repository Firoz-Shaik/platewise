from django.conf import settings
from django.db import models

from hostel.models import Hostel


class Membership(models.Model):
    class Role(models.TextChoices):
        HOSTEL_ADMIN = "hostel_admin", "Hostel administrator"
        MESS_MANAGER = "mess_manager", "Mess manager"
        ATTENDANCE_OPERATOR = "attendance_operator", "Attendance operator"
        ANALYST = "analyst", "Analyst"
        STUDENT = "student", "Student"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=32, choices=Role.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "hostel"], name="unique_user_hostel_membership")]

# Create your models here.
