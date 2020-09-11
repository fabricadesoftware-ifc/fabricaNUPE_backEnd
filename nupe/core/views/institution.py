from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import CampusFilter, InstitutionFilter
from nupe.core.models import Campus, Institution
from nupe.core.serializers import CampusListSerializer, CampusSerializer, InstitutionSerializer


class InstitutionViewSet(ModelViewSet):
    """
    list: retorna todas as instituições do banco de dados

    retrieve: retorna uma instituição especifica do banco de dados

    create: cadastra uma instituição no banco de dados

    destroy: exclui uma instituição do banco de dados

    partial_update: atualiza um ou mais atributos de uma instituição
    """

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    filterset_class = InstitutionFilter
    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_institution"],
        "retrieve": ["core.view_institution"],
        "create": ["core.add_institution"],
        "partial_update": ["core.change_institution"],
        "destroy": ["core.delete_institution"],
    }


class CampusViewSet(ModelViewSet):
    """
    list: retorna todos os campus do banco de dados

    retrieve: retorna um campus especifico do banco de dados

    create: cadastrar um campus no banco de dados

    destroy: exclui um campus do banco de dados

    partial_update: atualiza um ou mais atributos de um campus
    """

    queryset = Campus.objects.all()

    filterset_class = CampusFilter
    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_campus"],
        "retrieve": ["core.view_campus"],
        "create": ["core.add_campus"],
        "partial_update": ["core.change_campus"],
        "destroy": ["core.delete_campus"],
    }

    per_action_serializer = {
        "list": CampusListSerializer,
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, CampusSerializer)
