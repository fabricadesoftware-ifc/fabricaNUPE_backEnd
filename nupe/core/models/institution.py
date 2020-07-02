from django.db import models
from safedelete.models import NO_DELETE, SOFT_DELETE_CASCADE, SafeDeleteModel

INSTITUTION_MAX_LENGTH = 50
CAMPUS_MAX_LENGTH = 50


class Institution(SafeDeleteModel):
    """
    Model para definir o nome de uma instituição

    Exemplo: 'Instituto Federal Catarinense'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=INSTITUTION_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Campus(SafeDeleteModel):
    """
    Model para definir o nome de um campus

    Exemplo: 'Araquari'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
        location: localização (o2m)
        institutions: instituições desse campus (m2m)
        academic_education: cursos fornecidos por esse campus (m2m)
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=CAMPUS_MAX_LENGTH, unique=True)
    location = models.ForeignKey("Location", related_name="campus", on_delete=models.PROTECT)
    institutions = models.ManyToManyField("Institution", related_name="campus", through="InstitutionCampus")
    academic_education = models.ManyToManyField(
        "AcademicEducation", related_name="campus", through="AcademicEducationCampus",
    )

    def __str__(self):
        return self.name


class InstitutionCampus(SafeDeleteModel):
    """
    Model para definir uma instituição pertencente à um campus. É uma associativa entre a model de Institution e Campus

    Exemplo: 'Instituto Federal Catarinense - Campus Araquari'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        institution: objeto do tipo model Institution (o2m)
        campus: objeto do tipo model Campus (o2m)
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    institution = models.ForeignKey("Institution", related_name="institution_campus", on_delete=models.PROTECT)
    campus = models.ForeignKey("Campus", related_name="institution_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["institution", "campus"]

    def __str__(self):
        return f"{self.institution} - {self.campus}"


class AcademicEducationCampus(SafeDeleteModel):
    """
    Model para definir um curso que pertence à uma instituição de um campus.
    É uma associativa entre a model de AcademicEducation e Campus

    Exemplo: 'Sistemas de Informação - Campus Araquari'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        academic_education: objeto do tipo model 'AcademicEducation' (o2m)
        campus: objeto do tipo model 'Campus' (o2m)
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    academic_education = models.ForeignKey("AcademicEducation", related_name="course_campus", on_delete=models.CASCADE)
    campus = models.ForeignKey("Campus", related_name="course_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["campus", "academic_education"]

    def __str__(self):
        return f"{self.academic_education} - {self.campus}"
