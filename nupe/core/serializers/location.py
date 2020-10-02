from rest_framework.serializers import CharField, ModelSerializer

from nupe.core.models import City, Location, State


class CitySerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais cidade

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    class Meta:
        model = City
        fields = ["id", "name"]


class StateSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre um ou mais estado

    Campos:
        id: identificador (somente leitura)

        name: nome

        initials: sigla
    """

    class Meta:
        model = State
        fields = ["id", "name", "initials"]


class LocationSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais localização

    Campos:
        id: identificador (somente leitura)

        name: nome (somente leitura)
    """

    name = CharField(source="__str__", read_only=True)

    class Meta:
        model = Location
        fields = ["id", "name"]
