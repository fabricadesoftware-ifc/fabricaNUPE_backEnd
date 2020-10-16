from django_filters import CharFilter, FilterSet

from nupe.core.models import Attendance


class AttendanceFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Attendance. RF.SIS.011, RF.SIS.012, RF.SIS.026

    Exemplo:
        /api/v1/attendance?foo=xyz

        ou

        /api/v1/attendance?foo=xyz&bar=abc

    Parâmetros:
        student_name: igual a string fornecida (case insensitive)

        student_last_name: igual a string fornecida (case insensitive)

        attendant_name: igual a string fornecida (case insensitive)

        attendant_last_name: igual a string fornecida (case insensitive)

        severity: igual ao char fornecido

        status: igual ao char fornecido
    """

    student_name = CharFilter(field_name="student__person__first_name", lookup_expr="iexact")
    student_last_name = CharFilter(field_name="student__person__last_name", lookup_expr="iexact")
    attendant_name = CharFilter(field_name="attendants__person__first_name", lookup_expr="iexact")
    attendant_last_name = CharFilter(field_name="attendants__person__last_name", lookup_expr="iexact")
    severity = CharFilter(field_name="attendance_severity")

    class Meta:
        model = Attendance
        fields = [
            "student",
            "student_name",
            "student_last_name",
            "attendants",
            "attendant_name",
            "attendant_last_name",
            "status",
            "severity",
        ]
