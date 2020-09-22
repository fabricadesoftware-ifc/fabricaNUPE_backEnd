from rest_framework.serializers import CharField, ModelSerializer

from nupe.core.models import City, Location, State


class CitySerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais cidade

    Campos:
        id: identificador

        name: nome
    """

    class Meta:
        model = City
        fields = ["id", "name"]

    def create(self, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover

    def update(self, instance, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover


class StateSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre um ou mais estado

    Campos:
        id: identificador

        name: nome

        initials: sigla
    """

    class Meta:
        model = State
        fields = ["id", "name", "initials"]

    def create(self, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover

    def update(self, instance, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover


class LocationSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais localização

    Campos:
        id: identificador

        name: nome
    """

    name = CharField(source="__str__", read_only=True)

    class Meta:
        model = Location
        fields = ["id", "name"]

    def create(self, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover

    def update(self, instance, validated_data):
        """
        Raises:
            NotImplementedError: Serializer somente leitura
        """
        raise NotImplementedError("Serializer somente leitura")  # pragma: no cover
