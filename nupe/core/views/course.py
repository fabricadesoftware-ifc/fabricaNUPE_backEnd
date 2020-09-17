from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from nupe.core.filters import AcademicEducationFilter, CourseFilter, GradeFilter
from nupe.core.models import AcademicEducation, Course, Grade
from nupe.core.serializers import AcademicEducationSerializer, CourseSerializer, GradeSerializer


class CourseViewSet(ModelViewSet):
    """
    list: retorna todos os cursos do banco de dados

    retrieve: retorna um curso especifico do banco de dados

    create: cadastra um curso no banco de dados

    destroy: exclui um curso do banco de dados

    partial_update: atualiza um ou mais atributos de um curso
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_course"],
        "retrieve": ["core.view_course"],
        "create": ["core.add_course"],
        "partial_update": ["core.change_course"],
        "destroy": ["core.delete_course"],
    }


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
    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_grade"],
        "retrieve": ["core.view_grade"],
        "create": ["core.add_grade"],
        "partial_update": ["core.change_grade"],
        "destroy": ["core.delete_grade"],
    }


class AcademicEducationViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    list: retorna todas as formações acadêmicas do banco de dados

    retrieve: retorna uma formação acadêmica específica do banco de dados
    """

    queryset = AcademicEducation.objects.all()
    serializer_class = AcademicEducationSerializer
    filterset_class = AcademicEducationFilter
    ordering = ["grade__name", "course__name"]

    perms_map_action = {
        "list": ["core.view_academiceducation"],
        "retrieve": ["core.view_academiceducation"],
    }
