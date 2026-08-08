from datetime import date

from django.db.models import Count, Sum

from hostel.models import Hostel
from meals.models import MealSession


def operational_summary(*, hostel: Hostel, service_date: date) -> dict:
    sessions = MealSession.objects.filter(hostel=hostel, service_date=service_date).annotate(attendance_count=Count("attendance_records"))
    totals = sessions.aggregate(
        prepared=Sum("prepared_quantity"),
        served=Sum("served_quantity"),
        waste=Sum("waste_quantity"),
        diners=Sum("attendance_count"),
    )
    prepared, waste = totals["prepared"] or 0, totals["waste"] or 0
    return {
        "date": service_date,
        "sessions": sessions.count(),
        "open_sessions": sessions.filter(status=MealSession.Status.OPEN).count(),
        "attendance": totals["diners"] or 0,
        "prepared": prepared,
        "served": totals["served"] or 0,
        "waste": waste,
        "waste_rate": round(float(waste / prepared * 100), 1) if prepared else None,
    }
