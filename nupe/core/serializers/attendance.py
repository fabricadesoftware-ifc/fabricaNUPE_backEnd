from django.shortcuts import get_object_or_404
from rest_framework.serializers import CharField, ModelSerializer, StringRelatedField

from nupe.account.models.account import Account
from nupe.core.models import Attendance


class AttendanceCreateSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendance_reason",
            "attendance_severity",
            "attendants",
            "student",
            "status",
        ]

    def create(self, validated_data):
        if validated_data.get("attendants") is not None:
            attendants = validated_data.pop("attendants")

            attendance = Attendance.objects.create(**validated_data)

            for attendant_id in attendants:
                attendance.attendants.add(get_object_or_404(Account, pk=attendant_id))

            return attendance

        return Attendance.objects.create(**validated_data)


class AttendanceListSerializer(ModelSerializer):
    attendants = StringRelatedField(many=True)
    student = CharField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendants",
            "student",
            "status",
        ]


class AttendanceDetailSerializer(ModelSerializer):
    attendance_reason = CharField()
    attendants = StringRelatedField(many=True)
    student = CharField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendance_reason",
            "attendance_severity",
            "attendants",
            "student",
            "status",
            "opened_at",
            "closed_at",
        ]
