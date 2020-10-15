from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class Grade(SafeDeleteModel):
    """
    Define o nível/grau de um curso

    Exemplo:
        'Bacharelado'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        name: nomenclatura

        academic_education: relação inversa para a model AcademicEducation
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class AcademicEducation(SafeDeleteModel):
    """
    Define o nome de uma formação acadêmica

    Exemplo:
        'Bacharelado em Sistemas de Informação'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        name: nome do curso

        grade: grau do curso

        campi: campi onde oferecem a formação

        academic_education_campus: relação inversa para a model AcademicEducationCampus
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=50, unique=True)
    grade = models.ForeignKey("Grade", related_name="academic_education", on_delete=models.CASCADE)
    campi = models.ManyToManyField("Campus", related_name="academic_education", through="AcademicEducationCampus",)

    def __str__(self) -> str:
        return f"{self.grade} em {self.name}"


class AcademicEducationCampus(SafeDeleteModel):
    """
    Define uma formação acadêmica que pertence à um campus. É uma associativa entre a model de
    AcademicEducation e Campus

    Exemplo:
        'Bacharelado em Sistemas de Informação - IFC - Araquari'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        academic_education: objeto do tipo model 'AcademicEducation' (o2m)

        campus: objeto do tipo model 'Campus' (o2m)

        students: relação inversa para a model Student
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    academic_education = models.ForeignKey(
        "AcademicEducation", related_name="academic_education_campus", on_delete=models.CASCADE,
    )
    campus = models.ForeignKey("Campus", related_name="academic_education_campus", on_delete=models.PROTECT,)

    class Meta:
        unique_together = ["academic_education", "campus"]

    def __str__(self) -> str:
        return f"{self.academic_education} - {self.campus}"
