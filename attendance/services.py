from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from attendance.models import AttendanceRecord
from meals.models import MealSession
from students.models import Student


@transaction.atomic
def record_attendance(*, session: MealSession, student: Student, actor, method: str = "staff_entry") -> AttendanceRecord:
    if session.status != MealSession.Status.OPEN:
        raise ValidationError({"session": "Attendance is available only while a session is open."})
    if student.hostel_id != session.hostel_id or student.status != Student.Status.ACTIVE:
        raise ValidationError({"student": "Student is not active in this hostel."})
    try:
        return AttendanceRecord.objects.create(meal_session=session, student=student, actor=actor, method=method)
    except IntegrityError as exc:
        raise ValidationError({"student": "Attendance is already recorded for this session."}, code="duplicate_attendance") from exc
