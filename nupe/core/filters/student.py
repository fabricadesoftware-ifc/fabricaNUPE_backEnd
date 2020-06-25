from django_filters import CharFilter, DateFromToRangeFilter, FilterSet, NumberFilter

from nupe.core.models import Student


class StudentFilter(FilterSet):
    ingress_date = DateFromToRangeFilter()
    course_id = NumberFilter(field_name="academic_education_campus__academic_education")
    campus_name = CharFilter(field_name="academic_education_campus__campus__name", lookup_expr="iexact")

    class Meta:
        model = Student
        fields = ["graduated", "ingress_date", "course_id", "campus_name"]
