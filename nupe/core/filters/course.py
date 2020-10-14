from django_filters import CharFilter, FilterSet

from nupe.core.models import AcademicEducation, Course, Grade


class CourseFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Course

    Exemplo:
        /api/v1/course?foo=xyz

        ou

        /api/v1/course?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)
    """

    name = CharFilter(lookup_expr="iexact")

    class Meta:
        model = Course
        fields = ["name"]


class GradeFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Grade

    Exemplo:
        /api/v1/grade?foo=xyz

        ou

        /api/v1/grade?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)

        course_name = igual a string fornecida (case insensitive)
    """

    name = CharFilter(lookup_expr="iexact")
    course_name = CharFilter(field_name="courses__name", lookup_expr="iexact")

    class Meta:
        model = Grade
        fields = ["name", "course_name"]


class AcademicEducationFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de AcademicEducation

    Exemplo:
        /api/v1/academic_education?foo=xyz

        ou

        /api/v1/academic_education?foo=xyz&bar=abc

    Parâmetros:
        course_name = igual a string fornecida (case insensitive)

        grade_name = igual a string fornecida (case insensitive)
    """

    course_name = CharFilter(lookup_expr="iexact")
    grade_name = CharFilter(lookup_expr="iexact")

    class Meta:
        model = AcademicEducation
        fields = ["course_name", "grade_name"]
