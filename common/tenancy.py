from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from hostel.models import Hostel


def request_hostel(request) -> Hostel:
    """Resolve the explicit tenant context; never fall back to an unscoped query."""
    value = request.headers.get("X-Hostel-Id")
    if not value:
        raise ValidationError({"X-Hostel-Id": "This header is required."})
    try:
        hostel_id = int(value)
    except ValueError as exc:
        raise ValidationError({"X-Hostel-Id": "Must be an integer."}) from exc
    try:
        hostel = Hostel.objects.get(id=hostel_id, status=Hostel.Status.ACTIVE)
    except Hostel.DoesNotExist as exc:
        raise NotFound("Hostel not found.") from exc
    if not request.user.is_superuser and not request.user.memberships.filter(hostel=hostel, is_active=True).exists():
        raise PermissionDenied("You do not have access to this hostel.")
    return hostel
