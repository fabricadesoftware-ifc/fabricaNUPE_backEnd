from django_filters import FilterSet, NumberFilter

from nupe.core.models import AttendanceReason


class AttendanceReasonFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de AttendanceReason

    Exemplo:
        /api/v1/attendance_reason?foo=xyz

        ou

        /api/v1/attendance_reason?foo=xyz&bar=abc

    Parâmetros:
        father_reason: igual ao id fornecido
    """

    father_reason = NumberFilter(method="get_sons")

    class Meta:
        model = AttendanceReason
        fields = ["father_reason"]

    def get_sons(self, queryset, name, value):
        return AttendanceReason.objects.filter(father_reason=value)
