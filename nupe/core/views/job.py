from rest_framework.viewsets import ModelViewSet

from nupe.core.models import Function, Sector
from nupe.core.serializers import FunctionSerializer, SectorSerializer


class FunctionViewSet(ModelViewSet):
    """
    list: retorna todas as funções/cargos do banco de dados

    retrieve: retorna uma função/cargo especifica do banco de dados

    create: cadastra uma função/cargo no banco de dados

    destroy: exclui uma função/cargo do banco de dados

    partial_update: atualiza um ou mais atributos de uma função/cargo
    """

    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    perms_map_action = {
        "list": ["core.view_function"],
        "retrieve": ["core.view_function"],
        "create": ["core.add_function"],
        "partial_update": ["core.change_function"],
        "destroy": ["core.delete_function"],
    }


class SectorViewSet(ModelViewSet):
    """
    list: retorna todos os setores do banco de dados

    retrieve: retorna um setor especifico do banco de dados

    create: cadastra um setor no banco de dados

    destroy: exclui um setor do banco de dados

    partial_update: atualiza um ou mais atributos de um setor
    """

    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    perms_map_action = {
        "list": ["core.view_sector"],
        "retrieve": ["core.view_sector"],
        "create": ["core.add_sector"],
        "partial_update": ["core.change_sector"],
        "destroy": ["core.delete_sector"],
    }
