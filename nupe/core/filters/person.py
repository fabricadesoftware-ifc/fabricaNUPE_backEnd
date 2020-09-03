from django_filters import DateFromToRangeFilter, FilterSet

from nupe.core.models import Person


class PersonFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Person

    Exemplo:
        /api/v1/person?foo=xyz

        ou

        /api/v1/person?foo=xyz&bar=abc

    Parâmetros:
        birthday_date_before: menor a data especificada (yyyy-mm-dd)

        birthday_date_after: maior a data especificada (yyyy-mm-dd)

        gender: igual ao char especificado (F, M)
    """

    birthday_date = DateFromToRangeFilter()

    class Meta:
        model = Person
        fields = ["gender", "birthday_date"]
