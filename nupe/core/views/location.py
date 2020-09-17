from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from nupe.core.filters import CityFilter, LocationFilter, StateFilter
from nupe.core.models import City, Location, State
from nupe.core.serializers import CitySerializer, LocationSerializer, StateSerializer


class LocationViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    list: retorna todas as localizações do banco de dados

    retrieve: retorna uma localização especifica do banco de dados
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    filterset_class = LocationFilter

    ordering = "city__name"

    perms_map_action = {
        "list": ["core.view_location"],
        "retrieve": ["core.view_location"],
    }


class CityViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    list: retorna todas as cidades do banco de dados

    retrieve: retorna uma cidade especifica do banco de dados
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer

    filterset_class = CityFilter

    ordering = "name"

    perms_map_action = {
        "list": ["core.view_city"],
        "retrieve": ["core.view_city"],
    }


class StateViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    list: retorna todas os estados do banco de dados

    retrieve: retorna um estado especifico do banco de dados
    """

    queryset = State.objects.all()
    serializer_class = StateSerializer

    filterset_class = StateFilter

    ordering = "name"

    perms_map_action = {
        "list": ["core.view_state"],
        "retrieve": ["core.view_state"],
    }
