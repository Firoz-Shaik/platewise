from django.db import models

from hostel.models import Hostel


class MealSession(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", "Breakfast"
        LUNCH = "lunch", "Lunch"
        DINNER = "dinner", "Dinner"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT, related_name="meal_sessions")
    service_date = models.DateField()
    meal_type = models.CharField(max_length=16, choices=MealType.choices)
    location = models.CharField(max_length=80, default="Main dining hall")
    menu_name = models.CharField(max_length=160)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    forecast_diners = models.PositiveIntegerField(null=True, blank=True)
    prepared_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    served_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    waste_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=16, default="portions")
    opened_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["hostel", "service_date", "meal_type", "location"], name="unique_meal_session_natural_key")]
        indexes = [models.Index(fields=["hostel", "service_date"])]
        ordering = ["-service_date", "meal_type"]
