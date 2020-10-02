from rest_framework.serializers import ModelSerializer

from nupe.core.models import Function, Sector


class FunctionSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma função/cargo, e também
    detalha ou lista informações sobre uma ou mais funções/cargos

    Campos:
        id: identificador (somente leitura)

        name: nome

        description: descrição
    """

    class Meta:
        model = Function
        fields = ["id", "name", "description"]


class SectorSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um setor, e também
    detalha ou lista informações sobre um ou mais setores

    Campos:
        id: identificador (somente leitura)

        name: nome

        description: descrição
    """

    class Meta:
        model = Sector
        fields = ["id", "name", "description"]
