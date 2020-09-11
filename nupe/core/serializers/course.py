from rest_framework.serializers import CharField, ModelSerializer

from nupe.core.models import AcademicEducation


class AcademicEducationSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais formação acadêmica

    Campos:
        id: identificador

        name: nome
    """

    name = CharField(source="__str__")

    class Meta:
        model = AcademicEducation
        fields = ["id", "name"]

    def create(self, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")

    def update(self, instance, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")
