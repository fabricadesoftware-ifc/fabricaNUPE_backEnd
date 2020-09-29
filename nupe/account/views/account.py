from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from nupe.account.filters import AccountFilter
from nupe.account.models import Account
from nupe.account.serializers import (
    AccountDetailSerializer,
    AccountListSerializer,
    AccountSerializer,
    CurrentAccountSerializer,
)


class AccountViewSet(ModelViewSet):
    """
    list: retorna todas as contas do banco de dados

    retrieve: retorna uma conta especifica do banco de dados

    create: cadastra uma conta no banco de dados

    destroy: exclui uma conta do banco de dados

    partial_update: atualiza um ou mais atributos de uma conta

    current: retorna informações sobre a conta logada atual
    """

    queryset = Account.objects.all()

    filterset_class = AccountFilter
    search_fields = ["email"]
    ordering_fields = ["email", "full_name"]
    ordering = ["full_name"]

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_account"],
        "retrieve": ["core.view_account"],
        "create": ["core.add_account"],
        "partial_update": ["core.change_account"],
        "destroy": ["core.delete_account"],
    }

    per_action_serializer = {
        "list": AccountListSerializer,
        "retrieve": AccountDetailSerializer,
        "create": AccountSerializer,
        "partial_update": AccountSerializer,
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action)

    @action(
        detail=False, url_path="current",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: CurrentAccountSerializer})
    def current(self, request):
        serializer = CurrentAccountSerializer(instance=self.request.user)
        data = {"user": serializer.data}

        return Response(data)
