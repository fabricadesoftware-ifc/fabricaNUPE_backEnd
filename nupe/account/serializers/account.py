from rest_framework.serializers import CharField, ModelSerializer

from nupe.account.models import Account
from nupe.core.serializers import PersonDetailSerializer


class AccountSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma conta

    Campos:
        id: identificador

        email: identificação para login

        person: identificador para a model Person com informações pessoais do usuário

        local_job: identificador para a model InstitutionCampus com o local onde trabalha

        function: identificador para a model Function com o cargo que ocupa

        sector: identificador para a model Sector com o setor onde trabalha
    """

    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "person",
            "local_job",
            "function",
            "sector",
        ]


class AccountDetailSerializer(ModelSerializer):
    """
    Retorna os detalhes de uma conta específica

    Campos:
        id: identificador

        email: identificação para login

        person: informações pessoais do usuário

        local_job: local onde trabalha

        function: cargo que ocupa

        sector: setor onde trabalha
    """

    person = PersonDetailSerializer()
    local_job = CharField()
    function = CharField()
    sector = CharField()

    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "person",
            "local_job",
            "function",
            "sector",
        ]


class AccountListSerializer(ModelSerializer):
    """
    Retorna uma lista de contas cadastradas no banco de dados

    Campos:
        id: identificador

        full_name: nome completo do usuário

        email: identificação para login

        local_job: local onde trabalha
    """

    local_job = CharField()

    class Meta:
        model = Account
        fields = ["id", "full_name", "email", "local_job"]


class CurrentAccountSerializer(ModelSerializer):
    """
    Retorna informações sobre o usuário logado atual

    Campos:
        id: identificador

        email: identificação para login

        person: informações pessoais do usuário

        local_job: instituição/campus onde trabalha

        date_joined: data da criação da conta

        is_active: conta ativa ou não

        is_staff: é ou não é um funcionário

        is_superuser: é ou não é um administrador do sistema
    """

    person = PersonDetailSerializer()
    local_job = CharField()
    function = CharField()
    sector = CharField()

    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "person",
            "local_job",
            "function",
            "sector",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
