from rest_framework.viewsets import ModelViewSet

from nupe.core.models import Attendance
from nupe.core.serializers import AttendanceCreateSerializer, AttendanceDetailSerializer, AttendanceListSerializer


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()

    per_action_serializer = {"list": AttendanceListSerializer, "retrieve": AttendanceDetailSerializer}

    http_method_names = ["get", "post", "patch", "delete"]

    ordering = "attendance_severity"

    perms_map_action = {
        "list": ["core.view_attendance"],
        "retrieve": ["core.view_attendance"],
        "create": ["core.add_attendance"],
        "partial_update": ["core.change_attendance"],
        "destroy": ["core.delete_attendance"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, AttendanceCreateSerializer)
