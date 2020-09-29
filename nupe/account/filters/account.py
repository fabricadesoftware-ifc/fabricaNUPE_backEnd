from django_filters import CharFilter, FilterSet

from nupe.account.models import Account


class AccountFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Account

    Exemplo:
        /api/v1/account?foo=xyz

        ou

        /api/v1/account?foo=xyz&bar=abc

    Parâmetros:
        campus_name: igual a string fornecida (case insensitive)

        institution_name: igual a string fornecida (case insensitive)

        function: igual a string fornecida (case insensitive)

        sector: igual a string fornecida (case insensitive)
    """

    campus_name = CharFilter(field_name="local_job__campus__name", lookup_expr="iexact")
    institution_name = CharFilter(field_name="local_job__institution__name", lookup_expr="iexact")
    function = CharFilter(field_name="function__name", lookup_expr="iexact")
    sector = CharFilter(field_name="sector__name", lookup_expr="iexact")

    class Meta:
        model = Account
        fields = ["campus_name", "institution_name", "function", "sector"]
