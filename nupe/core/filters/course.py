from django_filters import CharFilter, FilterSet

from nupe.core.models import AcademicEducation, Grade


class GradeFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Grade

    Exemplo:
        /api/v1/grade?foo=xyz

        ou

        /api/v1/grade?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)

        academic_education_name = igual a string fornecida (case insensitive)
    """

    name = CharFilter(lookup_expr="iexact")
    academic_education_name = CharFilter(field_name="academic_education__name", lookup_expr="iexact")

    class Meta:
        model = Grade
        fields = ["name", "academic_education_name"]


class AcademicEducationFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de AcademicEducation

    Exemplo:
        /api/v1/academic_education?foo=xyz

        ou

        /api/v1/academic_education?foo=xyz&bar=abc

    Parâmetros:
        name = igual a string fornecida (case insensitive)

        grade_name = igual a string fornecida (case insensitive)
    """

    name = CharFilter(lookup_expr="iexact")
    grade_name = CharFilter(field_name="grade__name", lookup_expr="iexact")

    class Meta:
        model = AcademicEducation
        fields = ["name", "grade_name"]
