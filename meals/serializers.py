from rest_framework import serializers

from meals.models import MealSession


class MealSessionSerializer(serializers.ModelSerializer):
    attendance_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = MealSession
        fields = ["id", "service_date", "meal_type", "location", "menu_name", "status", "forecast_diners", "prepared_quantity", "served_quantity", "waste_quantity", "unit", "attendance_count"]
        read_only_fields = ["id", "status", "attendance_count"]
