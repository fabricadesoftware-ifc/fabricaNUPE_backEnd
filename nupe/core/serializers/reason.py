from rest_framework.serializers import CharField, ModelSerializer

from nupe.core.models import AttendanceReason, CrisisType, DrugType, SpecialNeedType


class SpecialNeedTypeSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um tipo de necessidade especial, e também
    lista ou detalha informações sobre um ou mais tipos de necessidades especiais

    Campos:
        id: identificador (somente leitura)

        name: nome

        description: descrição
    """

    class Meta:
        model = SpecialNeedType
        fields = ["id", "name", "description"]


class CrisisTypeSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um tipo de crise, e também
    lista ou detalha informações sobre um ou mais tipos de crises

    Campos:
        id: identificador (somente leitura)

        name: nome

        description: descrição
    """

    class Meta:
        model = CrisisType
        fields = ["id", "name", "description"]


class DrugTypeSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um tipo de droga, e também
    lista ou detalha informações sobre um ou mais tipos de drogas

    Campos:
        id: identificador (somente leitura)

        name: nome

        description: descrição
    """

    class Meta:
        model = DrugType
        fields = ["id", "name", "description"]


class AttendanceCreateReasonSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um motivo de atendimento

    Campos:
        id: identificador (somente leitura)

        description: descrição

        special_need: necessidades especiais a ser atendida

        crisis: crises a ser atendida

        drug: tipos de drogas que o aluno que será atendido utilizou
    """

    class Meta:
        model = AttendanceReason
        fields = ["id", "description", "special_need", "crisis", "drug"]


class AttendanceReasonSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre um ou mais motivos de atendimento

    Campos:
        id: identificador (somente leitura)

        description: descrição

        special_need: necessidades especiais a ser atendida

        crisis: crises a ser atendida

        drug: tipos de drogas que o aluno que será atendido utilizou
    """

    special_need = CharField()
    crisis = CharField()
    drug = CharField()

    class Meta:
        model = AttendanceReason
        fields = ["id", "description", "special_need", "crisis", "drug"]
