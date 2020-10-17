from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import AcademicEducationFilter, GradeFilter
from nupe.core.models import AcademicEducation, Grade
from nupe.core.serializers.course import (
    AcademicEducationCreateSerializer,
    AcademicEducationDetailSerializer,
    AcademicEducationListSerializer,
    GradeSerializer,
)


class GradeViewSet(ModelViewSet):
    """
    list: retorna todos os graus do banco de dados. RF.SIS.035, RF.SIS.036, RF.SIS.037, RF.SIS.038

    retrieve: retorna um grau especifico do banco de dados

    create: cadastra um grau no banco de dados. RF.SIS.034

    destroy: exclui um grau do banco de dados. RF.SIS.040

    partial_update: atualiza um ou mais atributos de um grau. RF.SIS.039
    """

    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filterset_class = GradeFilter
    search_fields = ["name"]  # RF.SIS.037
    ordering_fields = ["name"]  # RF.SIS.038
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
    list: retorna todas as formações acadêmicas do banco de dados. RF.SIS.028, RF.SIS.029, RF.SIS.030, RF.SIS.031

    retrieve: retorna uma formação acadêmica específica do banco de dados

    create: cadastra uma formação acadêmica no banco de dados. RF.SIS.027

    destroy: exclui uma formação acadêmica do banco de dados. RF.SIS.033

    partial_update: atualiza um ou mais atributos de uma formação acadêmica. RF.SIS.032
    """

    queryset = AcademicEducation.objects.all()
    filterset_class = AcademicEducationFilter
    search_fields = ["grade__name", "name"]  # RF.SIS.030
    ordering_fields = ["grade__name", "name"]  # RF.SIS.031
    ordering = ["grade__name", "name"]

    per_action_serializer = {
        "list": AcademicEducationListSerializer,
        "retrieve": AcademicEducationDetailSerializer,
        "create": AcademicEducationCreateSerializer,
        "partial_update": AcademicEducationCreateSerializer,
    }

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_academiceducation"],
        "retrieve": ["core.view_academiceducation"],
        "create": ["core.add_academiceducation"],
        "partial_update": ["core.change_academiceducation"],
        "destroy": ["core.delete_academiceducation"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action)
