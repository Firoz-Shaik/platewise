from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from meals.models import MealSession


@transaction.atomic
def open_session(session: MealSession) -> MealSession:
    if session.status != MealSession.Status.DRAFT:
        raise ValidationError({"status": "Only draft sessions can be opened."})
    session.status, session.opened_at = MealSession.Status.OPEN, timezone.now()
    session.save(update_fields=["status", "opened_at"])
    return session


@transaction.atomic
def close_session(session: MealSession, *, prepared, served, waste, unit: str) -> MealSession:
    if session.status != MealSession.Status.OPEN:
        raise ValidationError({"status": "Only open sessions can be closed."})
    if min(prepared, served, waste) < 0 or served + waste > prepared:
        raise ValidationError({"quantities": "Quantities must be non-negative and served plus waste cannot exceed prepared."})
    session.status, session.closed_at = MealSession.Status.CLOSED, timezone.now()
    session.prepared_quantity, session.served_quantity, session.waste_quantity, session.unit = prepared, served, waste, unit
    session.save()
    return session
