from datetime import date

from rest_framework import permissions, response
from rest_framework.views import APIView

from analytics.selectors import operational_summary
from common.tenancy import request_hostel


class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        value = request.query_params.get("date")
        try:
            service_date = date.fromisoformat(value) if value else date.today()
        except ValueError:
            return response.Response({"date": "Use ISO-8601 YYYY-MM-DD."}, status=400)
        return response.Response(operational_summary(hostel=request_hostel(request), service_date=service_date))
