from django.urls import path

from analytics.views import SummaryView

urlpatterns = [path("summary", SummaryView.as_view())]
