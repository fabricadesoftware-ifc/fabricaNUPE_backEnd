from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from nupe.core.models import AcademicEducation, Campus, Grade
from nupe.core.serializers.institution import CampusDetailSerializer, CampusListSerializer


class GradeSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um grau de formação, e também
    detalha ou lista informações sobre um ou mais graus

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    class Meta:
        model = Grade
        fields = ["id", "name"]


class AcademicEducationCreateSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma formação acadêmica

    Campos:
        id: identificador (somente leitura)

        name: nome

        grade: identificador do objeto da model Grade

        campi: lista de id dos campi
    """

    campi = PrimaryKeyRelatedField(queryset=Campus.objects.all(), many=True)

    class Meta:
        model = AcademicEducation
        fields = ["id", "name", "grade", "campi"]


class AcademicEducationListSerializer(ModelSerializer):
    """
    Retorna uma lista de informações sobre formações acadêmicas

    Campos:
        id: identificador

        name: nome da formação acadêmica

        grade: informações sobre o grau da formação acadêmica

        campi: informações sobre os campi que oferecem a formação acadêmica
    """

    grade = GradeSerializer()
    campi = CampusListSerializer(many=True)

    class Meta:
        model = AcademicEducation
        fields = ["id", "name", "grade", "campi"]


class AcademicEducationDetailSerializer(ModelSerializer):
    """
    Detalha informações sobre uma formação acadêmica específica

    Campos:
        id: identificador

        name: nome

        grade: informações sobre o grau da formação acadêmica

        campi: informações sobre os campi que oferecem a formação acadêmica
    """

    grade = GradeSerializer()
    campi = CampusDetailSerializer(many=True)

    class Meta:
        model = AcademicEducation
        fields = ["id", "name", "grade", "campi"]
