from django_filters import CharFilter, FilterSet

from nupe.core.models import City, Location, State


class LocationFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Location

    Exemplo:
        /api/v1/location?foo=xyz

        ou

        /api/v1/location?foo=xyz&bar=abc

    Parâmetros:
        city_name: igual a string fornecida (case insensitive)

        state_initials: igual a string fornecida (case insensitive)
    """

    city_name = CharFilter(field_name="city__name", lookup_expr="iexact")
    state_initials = CharFilter(field_name="state__initials", lookup_expr="iexact")

    class Meta:
        model = Location
        fields = ["city_name", "state_initials"]


class CityFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de City

    Exemplo:
        /api/v1/city?foo=xyz

        ou

        /api/v1/city?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)
    """

    name = CharFilter(field_name="name", lookup_expr="iexact")

    class Meta:
        model = City
        fields = ["name"]


class StateFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de State

    Exemplo:
        /api/v1/state?foo=xyz

        ou

        /api/v1/state?foo=xyz&bar=abc

    Parâmetros:
        initials: igual a string fornecida (case insensitive)
    """

    initials = CharFilter(field_name="initials", lookup_expr="iexact")

    class Meta:
        model = State
        fields = ["initials"]
