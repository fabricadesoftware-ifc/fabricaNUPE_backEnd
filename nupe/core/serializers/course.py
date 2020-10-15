from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.core.models import AcademicEducation, Campus, Grade


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


class AcademicEducationSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma formação acadêmica, e também
    lista informações sobre formações acadêmicas

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


class AcademicEducationDetailSerializer(ModelSerializer):
    """
    Detalha informações sobre uma formação acadêmica específica

    Campos:
        id: identificador

        name: nome

        grade: identificador do grau

        campi: identificadores dos campi
    """

    grade = CharField()
    campi = StringRelatedField(many=True)

    class Meta:
        model = AcademicEducation
        fields = ["id", "name", "grade", "campi"]
