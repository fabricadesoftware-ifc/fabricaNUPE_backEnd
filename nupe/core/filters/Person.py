from django_filters import DateFromToRangeFilter, FilterSet

from nupe.core.models import Person


class PersonFilter(FilterSet):
    birthday_date = DateFromToRangeFilter()

    class Meta:
        model = Person
        fields = ["gender", "birthday_date"]
