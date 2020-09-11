from django_filters import CharFilter, FilterSet

from nupe.core.models import Campus, Institution


class InstitutionFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Institution

    Exemplo:
        /api/v1/institution?foo=xyz

        ou

        /api/v1/institution?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)

        campus_name: igual a string fornecida (case insensitive)
    """

    name = CharFilter(field_name="name", lookup_expr="iexact")
    campus_name = CharFilter(field_name="campus__name", lookup_expr="iexact")

    class Meta:
        model = Institution
        fields = ["name", "campus_name"]


class CampusFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Campus

    Exemplo:
        /api/v1/campus?foo=xyz

        ou

        /api/v1/campus?foo=xyz&bar=abc

    Parâmetros:
        name: igual a string fornecida (case insensitive)
    """

    name = CharFilter(field_name="name", lookup_expr="iexact")

    class Meta:
        model = Campus
        fields = ["name"]
