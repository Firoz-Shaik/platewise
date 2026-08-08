from django.db.models import Count
from rest_framework import generics, permissions, response
from rest_framework.views import APIView

from common.tenancy import request_hostel
from meals.models import MealSession
from meals.serializers import MealSessionSerializer
from meals.services import close_session, open_session


class MealSessionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MealSessionSerializer

    def get_queryset(self):
        return MealSession.objects.filter(hostel=request_hostel(self.request)).annotate(attendance_count=Count("attendance_records"))

    def perform_create(self, serializer):
        serializer.save(hostel=request_hostel(self.request))


class SessionActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id, action):
        session = MealSession.objects.get(id=session_id, hostel=request_hostel(request))
        if action == "open":
            session = open_session(session)
        elif action == "close":
            session = close_session(session, **request.data)
        else:
            return response.Response({"detail": "Unknown action."}, status=400)
        return response.Response(MealSessionSerializer(session).data)
