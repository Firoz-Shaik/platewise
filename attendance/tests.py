from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from attendance.services import record_attendance
from hostel.models import Hostel
from meals.models import MealSession
from students.models import Student


class AttendanceServiceTests(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(name="North Hostel")
        self.user = get_user_model().objects.create_user(username="operator", password="safe-password")
        self.student = Student.objects.create(hostel=self.hostel, external_id="S-01", full_name="Asha Rao")
        self.session = MealSession.objects.create(hostel=self.hostel, service_date=date.today(), meal_type="lunch", menu_name="Lunch", status=MealSession.Status.OPEN)

    def test_duplicate_attendance_is_rejected(self):
        record_attendance(session=self.session, student=self.student, actor=self.user)
        with self.assertRaises(ValidationError):
            record_attendance(session=self.session, student=self.student, actor=self.user)
