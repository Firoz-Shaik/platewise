import csv
import hashlib
from io import TextIOWrapper

from django.db import transaction
from rest_framework.exceptions import ValidationError

from hostel.models import Hostel
from students.models import RosterImport, Student


REQUIRED_COLUMNS = {"external_id", "full_name"}


def preview_roster(uploaded_file) -> tuple[str, list[dict], list[dict]]:
    if uploaded_file is None:
        raise ValidationError({"file": "A CSV file is required."})
    if uploaded_file.size > 2 * 1024 * 1024:
        raise ValidationError({"file": "Roster files must be 2 MB or smaller."})
    if not uploaded_file.name.lower().endswith(".csv"):
        raise ValidationError({"file": "V1 supports CSV imports. XLSX support is an explicit next increment."})
    raw = uploaded_file.read()
    digest = hashlib.sha256(raw).hexdigest()
    rows = list(csv.DictReader(TextIOWrapper(__import__("io").BytesIO(raw), encoding="utf-8-sig")))
    if not rows or not REQUIRED_COLUMNS.issubset(rows[0].keys()):
        raise ValidationError({"file": "CSV must include external_id and full_name columns."})
    valid, errors, seen = [], [], set()
    for number, row in enumerate(rows, start=2):
        external_id, full_name = row.get("external_id", "").strip(), row.get("full_name", "").strip()
        if not external_id or not full_name or external_id in seen:
            errors.append({"row": number, "message": "external_id and full_name are required and external_id must be unique in the file."})
            continue
        seen.add(external_id)
        valid.append({"external_id": external_id, "full_name": full_name, "email": row.get("email", "").strip(), "room_number": row.get("room_number", "").strip()})
    return digest, valid, errors


@transaction.atomic
def commit_roster(*, hostel: Hostel, digest: str, rows: list[dict]) -> RosterImport:
    roster, created = RosterImport.objects.get_or_create(hostel=hostel, digest=digest)
    if not created and roster.status == RosterImport.Status.COMMITTED:
        return roster
    for row in rows:
        Student.objects.update_or_create(hostel=hostel, external_id=row["external_id"], defaults=row)
    roster.status, roster.accepted_rows, roster.rejected_rows = RosterImport.Status.COMMITTED, len(rows), 0
    roster.save(update_fields=["status", "accepted_rows", "rejected_rows"])
    return roster
