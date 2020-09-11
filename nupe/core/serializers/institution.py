from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.core.models import AcademicEducation, Campus, Institution
from nupe.core.serializers import AcademicEducationSerializer


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

        academic_education: identificadores das formações acadêmicas desse campus
    """

    institutions = PrimaryKeyRelatedField(
        many=True, queryset=Institution.objects.all(), write_only=True, required=False
    )
    academic_education = PrimaryKeyRelatedField(
        many=True, queryset=AcademicEducation.objects.all(), write_only=True, required=False
    )

    institution_output = InstitutionSerializer(source="institutions", many=True, read_only=True)
    academic_education_output = AcademicEducationSerializer(source="academic_education", many=True, read_only=True)

    class Meta:
        model = Campus
        fields = [
            "id",
            "name",
            "location",
            "institutions",
            "academic_education",
            "institution_output",
            "academic_education_output",
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
