from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import AttendanceFilter
from nupe.core.models import Attendance
from nupe.core.serializers import AttendanceCreateSerializer, AttendanceDetailSerializer, AttendanceListSerializer


class AttendanceViewSet(ModelViewSet):
    """
    list: retorna todas os atendimentos do banco de dados

    retrieve: retorna um atendimento especifico do banco de dados

    create: cadastra um atendimento no banco de dados

    destroy: exclui um atendimento do banco de dados

    partial_update: atualiza um ou mais atributos de um atendimento
    """

    queryset = Attendance.objects.all()
    filterset_class = AttendanceFilter
    search_fields = ["student__full_name", "attendants__full_name"]
    ordering_fields = [
        "student__person__full_name",
        "attendants__full_name",
        "attendance_severity",
        "status",
        "opened_at",
        "closed_at",
    ]
    ordering = "attendance_severity"

    per_action_serializer = {"list": AttendanceListSerializer, "retrieve": AttendanceDetailSerializer}

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_attendance"],
        "retrieve": ["core.view_attendance"],
        "create": ["core.add_attendance"],
        "partial_update": ["core.change_attendance"],
        "destroy": ["core.delete_attendance"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, AttendanceCreateSerializer)
