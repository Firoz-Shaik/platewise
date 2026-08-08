from django.conf import settings
from django.db import models

from meals.models import MealSession
from students.models import Student


class AttendanceRecord(models.Model):
    class Method(models.TextChoices):
        STAFF_ENTRY = "staff_entry", "Staff entry"
        QR = "qr", "QR"

    meal_session = models.ForeignKey(MealSession, on_delete=models.PROTECT, related_name="attendance_records")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="attendance_records")
    recorded_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.STAFF_ENTRY)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["meal_session", "student"], name="unique_student_attendance_per_session")]
