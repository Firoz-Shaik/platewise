from django.urls import path

from attendance.views import AttendanceCreateView
from meals.views import MealSessionListCreateView, SessionActionView

urlpatterns = [
    path("", MealSessionListCreateView.as_view()),
    path("<int:session_id>/attendance", AttendanceCreateView.as_view()),
    path("<int:session_id>/<str:action>", SessionActionView.as_view()),
]
