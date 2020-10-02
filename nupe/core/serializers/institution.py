from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.core.models import Campus, Institution


class InstitutionSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma instituição, e também
    detalha ou lista informações sobre uma ou mais instituições

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    class Meta:
        model = Institution
        fields = ["id", "name"]


class CampusSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um campus, e também
    detalha informações sobre um campus específico

    Campos:
        id: identificador (somente leitura)

        name: nome

        location: identificador da localização, 'Cidade - Estado'

        institutions: identificadores das instituições desse campus
    """

    institutions = PrimaryKeyRelatedField(queryset=Institution.objects.all(), many=True, required=False)

    class Meta:
        model = Campus
        fields = ["id", "name", "location", "institutions"]


class CampusListSerializer(ModelSerializer):
    """
    Retorna uma lista de campus cadastrados no banco de dados

    Campos:
        id: identificador (somente leitura)

        name: nome

        location: identificador da localização, 'Cidade - Estado'
    """

    location = StringRelatedField()

    class Meta:
        model = Campus
        fields = ["id", "name", "location"]
