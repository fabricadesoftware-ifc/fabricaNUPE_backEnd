from django_filters import DateFromToRangeFilter, FilterSet

from nupe.core.models import Person


class PersonFilter(FilterSet):
    """
    Filtros para requisições no endpoint de 'Person'

    Param:
        birthday_date_before: menor ou igual a data especificada (yyyy-mm-dd)
        birthday_date_after: maior ou igual a data especificada (yyyy-mm-dd)
        gender: igual ao char especificado (F, M)
    """

    birthday_date = DateFromToRangeFilter()

    class Meta:
        model = Person
        fields = ["gender", "birthday_date"]
