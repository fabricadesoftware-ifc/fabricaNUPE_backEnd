from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import AcademicEducationFilter, GradeFilter
from nupe.core.models import AcademicEducation, Grade
from nupe.core.serializers import AcademicEducationDetailSerializer, AcademicEducationSerializer, GradeSerializer


class GradeViewSet(ModelViewSet):
    """
    list: retorna todos os graus do banco de dados

    retrieve: retorna um grau especifico do banco de dados

    create: cadastra um grau no banco de dados

    destroy: exclui um grau do banco de dados

    partial_update: atualiza um ou mais atributos de um grau
    """

    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filterset_class = GradeFilter
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_grade"],
        "retrieve": ["core.view_grade"],
        "create": ["core.add_grade"],
        "partial_update": ["core.change_grade"],
        "destroy": ["core.delete_grade"],
    }


class AcademicEducationViewSet(ModelViewSet):
    """
    list: retorna todas as formações acadêmicas do banco de dados

    retrieve: retorna uma formação acadêmica específica do banco de dados

    create: cadastra uma formação acadêmica no banco de dados

    destroy: exclui uma formação acadêmica do banco de dados

    partial_update: atualiza um ou mais atributos de uma formação acadêmica
    """

    queryset = AcademicEducation.objects.all()
    serializer_class = AcademicEducationSerializer
    filterset_class = AcademicEducationFilter
    search_fields = ["grade__name", "name"]
    ordering_fields = ["grade__name", "name"]
    ordering = ["grade__name", "name"]

    per_action_serializer = {"retrieve": AcademicEducationDetailSerializer}

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_academiceducation"],
        "retrieve": ["core.view_academiceducation"],
        "create": ["core.add_academiceducation"],
        "partial_update": ["core.change_academiceducation"],
        "destroy": ["core.delete_academiceducation"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, self.serializer_class)
