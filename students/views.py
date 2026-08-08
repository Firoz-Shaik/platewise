from rest_framework import generics, permissions, response, status
from rest_framework.views import APIView

from common.tenancy import request_hostel
from students.models import Student
from students.serializers import StudentSerializer
from students.services import commit_roster, preview_roster


class StudentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer

    def get_queryset(self):
        hostel = request_hostel(self.request)
        query = self.request.query_params.get("q", "")
        return Student.objects.filter(hostel=hostel, full_name__icontains=query)

    def perform_create(self, serializer):
        serializer.save(hostel=request_hostel(self.request))


class RosterPreviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        digest, rows, errors = preview_roster(request.FILES.get("file"))
        return response.Response({"digest": digest, "accepted_rows": rows, "errors": errors})


class RosterCommitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        roster = commit_roster(hostel=request_hostel(request), digest=request.data["digest"], rows=request.data["rows"])
        return response.Response({"id": roster.id, "status": roster.status, "accepted_rows": roster.accepted_rows}, status=status.HTTP_201_CREATED)
