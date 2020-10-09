from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import AttendanceReasonFilter
from nupe.core.models import AttendanceReason
from nupe.core.serializers import AttendanceReasonSerializer


class AttendanceReasonViewSet(ModelViewSet):
    """
    list: retorna todos os motivos de atendimento pai do banco de dados

    retrieve: retorna um motivo de atendimento especifico do banco de dados

    create: cadastra um motivo de atendimento no banco de dados

    destroy: exclui um motivo de atendimento do banco de dados

    partial_update: atualiza um ou mais atributos de um motivo de atendimento
    """

    queryset = AttendanceReason.objects.all()
    serializer_class = AttendanceReasonSerializer
    filterset_class = AttendanceReasonFilter
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_attendancereason"],
        "retrieve": ["core.view_attendancereason"],
        "create": ["core.add_attendancereason"],
        "partial_update": ["core.change_attendancereason"],
        "destroy": ["core.delete_attendancereason"],
    }

    per_action_queryset = {
        "list": AttendanceReason.only_father.all(),
    }

    def get_queryset(self):
        return self.per_action_queryset.get(self.action, self.queryset)
