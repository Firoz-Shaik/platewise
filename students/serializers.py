from rest_framework import serializers

from students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "external_id", "full_name", "email", "room_number", "status", "created_at"]
        read_only_fields = ["id", "created_at"]
