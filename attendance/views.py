from rest_framework import permissions, response
from rest_framework.views import APIView

from attendance.services import record_attendance
from common.tenancy import request_hostel
from meals.models import MealSession
from students.models import Student


class AttendanceCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        hostel = request_hostel(request)
        session = MealSession.objects.get(id=session_id, hostel=hostel)
        student = Student.objects.get(id=request.data["student_id"], hostel=hostel)
        record = record_attendance(session=session, student=student, actor=request.user, method=request.data.get("method", "staff_entry"))
        return response.Response({"id": record.id, "student_id": record.student_id, "recorded_at": record.recorded_at}, status=201)
