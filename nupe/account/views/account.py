from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from nupe.account.filters import AccountFilter
from nupe.account.models import Account
from nupe.account.serializers.account import (
    AccountDetailSerializer,
    AccountListSerializer,
    AccountSerializer,
    CurrentAccountSerializer,
)


class AccountViewSet(ModelViewSet):
    """
    list: retorna todas as contas do banco de dados. RF.SIS.005, RF.SIS.006, RF.SIS.007, RF.SIS.008

    retrieve: retorna uma conta especifica do banco de dados

    create: cadastra uma conta no banco de dados. RF.SIS.004

    destroy: exclui uma conta do banco de dados. RF.SIS.010

    partial_update: atualiza um ou mais atributos de uma conta. RF.SIS.003, RF.SIS.009

    current: retorna informações sobre a conta logada atual
    """

    queryset = Account.objects.all()

    filterset_class = AccountFilter
    search_fields = ["email", "person__first_name", "person__last_name"]  # RF.SIS.008
    ordering_fields = ["email", "person__first_name", "person__last_name"]  # RF.SIS.007
    ordering = ["person__first_name", "person__last_name"]

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["account.view_account"],
        "retrieve": ["account.view_account"],
        "create": ["account.add_account"],
        "partial_update": ["account.change_account"],
        "destroy": ["account.delete_account"],
    }

    per_action_serializer = {
        "list": AccountListSerializer,
        "retrieve": AccountDetailSerializer,
        "create": AccountSerializer,
        "partial_update": AccountSerializer,
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action)

    @action(detail=False)
    @swagger_auto_schema(responses={HTTP_200_OK: CurrentAccountSerializer})
    def current(self, request):
        serializer = CurrentAccountSerializer(instance=self.request.user)
        data = {"user": serializer.data}

        return Response(data)
