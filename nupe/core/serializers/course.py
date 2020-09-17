from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.core.models import AcademicEducation, Course, Grade


class AcademicEducationSerializer(ModelSerializer):
    """
    Detalha ou lista informações sobre uma ou mais formação acadêmica

    Campos:
        id: identificador

        name: nome
    """

    name = CharField(source="__str__")

    class Meta:
        model = AcademicEducation
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


class CourseSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um curso, e também
    detalha ou lista informações sobre um ou mais cursos

    Campos:
        id: identificador

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
        id: identificador

        name: nome

        courses: identificadores dos cursos desse grau

        courses_output: nome dos cursos pertencentes ao grau
    """

    courses = PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, write_only=True, required=False)
    courses_output = StringRelatedField(source="courses", many=True, read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "name", "courses", "courses_output"]
