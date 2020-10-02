from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField

from nupe.core.models import AcademicEducation, Course, Grade


class CourseSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um curso, e também
    detalha ou lista informações sobre um ou mais cursos

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    class Meta:
        model = Course
        fields = ["id", "name"]


class GradeSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um grau de formação, e também
    detalha ou lista informações sobre um ou mais graus

    Campos:
        id: identificador (somente leitura)

        name: nome

        courses: identificadores dos cursos desse grau
    """

    courses = PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, required=False)

    class Meta:
        model = Grade
        fields = ["id", "name", "courses"]


class AcademicEducationSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais formação acadêmica

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    name = CharField(source="__str__")

    class Meta:
        model = AcademicEducation
        fields = ["id", "name"]
