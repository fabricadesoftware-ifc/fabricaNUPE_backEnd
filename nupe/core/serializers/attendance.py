from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.account.models.account import Account
from nupe.core.models import Attendance


class AttendanceCreateSerializer(ModelSerializer):
    attendants = PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)

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
