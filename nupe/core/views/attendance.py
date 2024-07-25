# from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import AttendanceFilter
from nupe.core.models import AccountAttendance, Attendance
from nupe.core.serializers.attendance import (
    AttendanceCreateSerializer,
    AttendanceDetailSerializer,
    AttendanceListSerializer,
    AttendanceReportSerializer,
    MyAccountAttendanceSerializer,
)


class AttendanceViewSet(ModelViewSet):
    """
    list: retorna todas os atendimentos do banco de dados. RF.SIS.021, RF.SIS.022, RF.SIS.023, RF.SIS.026, RF.SIS.011,
    RF.SIS.012

    retrieve: retorna um atendimento especifico do banco de dados

    create: cadastra um atendimento no banco de dados. RF.SIS.020

    destroy: exclui um atendimento do banco de dados. RF.SIS.025

    partial_update: atualiza um ou mais atributos de um atendimento. RF.SIS.024

    report: retorna um relatório completo de todos os atendimentos. RF.SIS.051, RF.SIS.052, RF.SIS.053, RF.SIS.054,
    RF.SIS.055, RF.SIS.056

    my: retorna todos os atendimentos realizados pelo usuário atual
    """

    queryset = Attendance.objects.all()
    filterset_class = AttendanceFilter  # RF.SIS.011, RF.SIS.012, RF.SIS.026
    search_fields = [
        "student__person__first_name",
        "student__person__last_name",
        "attendants__person__first_name",
        "attendants__person__last_name",
    ]
    ordering_fields = [
        "student__person__first_name",
        "student__person__last_name",
        "attendants__person__first_name",
        "attendants__person__last_name",
        "attendance_severity",
        "status",
        "opened_at",
        "closed_at",
    ]  # RF.SIS.023
    ordering = "attendance_severity"

    per_action_serializer = {"list": AttendanceListSerializer, "retrieve": AttendanceDetailSerializer}

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_attendance"],
        "retrieve": ["core.view_attendance"],
        "create": ["core.add_attendance"],
        "partial_update": ["core.change_attendance"],
        "destroy": ["core.delete_attendance"],
        "report": ["core.view_attendance"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, AttendanceCreateSerializer)

    @action(detail=False)
    # @swagger_auto_schema(responses={HTTP_200_OK: AttendanceReportSerializer})
    def report(self, request):
        queryset = self.filter_queryset(queryset=self.get_queryset())

        serializer = AttendanceReportSerializer(instance=queryset, many=True)

        return self.get_paginated_response(data=self.paginate_queryset(queryset=serializer.data))

    @action(detail=False)
    # @swagger_auto_schema(responses={HTTP_200_OK: MyAccountAttendanceSerializer})
    def my(self, request):
        serializer = MyAccountAttendanceSerializer(
            instance=AccountAttendance.objects.filter(account=request.user), many=True
        )

        return self.get_paginated_response(data=self.paginate_queryset(queryset=serializer.data))
