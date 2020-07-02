from django_filters import CharFilter, DateFromToRangeFilter, FilterSet, NumberFilter

from nupe.core.models import Student


class StudentFilter(FilterSet):
    """
    Filtros para requisições no endpoint de 'Student'

    Param:
        ingress_date_before: menor ou igual a data fornecida (yyyy-mm-dd)
        ingress_date_after: maior ou igual a data fornecida (yyyy-mm-dd)
        course_id: igual ao inteiro fornecido
        campus_name: igual a string fornecida (case insensitive)
        graduated: igual ao booleano fornecido (True, False)
    """

    ingress_date = DateFromToRangeFilter()
    course_id = NumberFilter(field_name="academic_education_campus__academic_education")
    campus_name = CharFilter(field_name="academic_education_campus__campus__name", lookup_expr="iexact")

    class Meta:
        model = Student
        fields = ["graduated", "ingress_date", "course_id", "campus_name"]
