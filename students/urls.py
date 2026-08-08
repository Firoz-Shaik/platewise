from django.urls import path

from students.views import RosterCommitView, RosterPreviewView, StudentListCreateView

urlpatterns = [
    path("", StudentListCreateView.as_view()),
    path("imports/preview", RosterPreviewView.as_view()),
    path("imports/commit", RosterCommitView.as_view()),
]
