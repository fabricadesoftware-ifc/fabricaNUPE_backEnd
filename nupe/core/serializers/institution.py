from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.core.models import Campus, Institution


class InstitutionSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma instituição, e também
    detalha ou lista informações sobre uma ou mais instituições

    Campos:
        id: identificador

        name: nome
    """

    class Meta:
        model = Institution
        fields = ["id", "name"]


class CampusSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar/atualizar um campus, e também
    detalha informações sobre um campus específico

    Campos:
        id: identificador

        name: nome

        location: identificador da localização, 'Cidade - Estado'

        institutions: identificadores das instituições desse campus

        institution_output: nome das instituições desse campus
    """

    institutions = PrimaryKeyRelatedField(
        many=True, queryset=Institution.objects.all(), write_only=True, required=False
    )
    institution_output = InstitutionSerializer(source="institutions", many=True, read_only=True)

    class Meta:
        model = Campus
        fields = [
            "id",
            "name",
            "location",
            "institutions",
            "institution_output",
        ]


class CampusListSerializer(ModelSerializer):
    """
    Retorna uma lista de campus cadastrados no banco de dados

    Campos:
        id: identificador

        name: nome

        location: identificador da localização, 'Cidade - Estado'
    """

    location = StringRelatedField()

    class Meta:
        model = Campus
        fields = ["id", "name", "location"]

    def create(self, validated_data):
        """
        Raises:
            NotImplementedError: Usar 'CampusSerializer' ao invés de 'CampusListSerializer'
        """
        raise NotImplementedError("Usar 'CampusSerializer' ao invés de 'CampusListSerializer'")  # pragma: no cover

    def update(self, instance, validated_data):
        """
        Raises:
            NotImplementedError: Usar 'CampusSerializer' ao invés de 'CampusListSerializer'
        """
        raise NotImplementedError("Usar 'CampusSerializer' ao invés de 'CampusListSerializer'")  # pragma: no cover
