from django.db import models
from safedelete.models import NO_DELETE, SOFT_DELETE_CASCADE, SafeDeleteModel

INSTITUTION_MAX_LENGTH = 50
CAMPUS_MAX_LENGTH = 50


class Institution(SafeDeleteModel):
    """
    Define o nome de uma instituição

    Exemplo:
        'Instituto Federal Catarinense'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome

        campus: relação inversa para a model Campus

        institutions_campus: relação inversa para a model InstitutionCampus
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=INSTITUTION_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Campus(SafeDeleteModel):
    """
    Define o nome de um campus para ser atribuído a uma instituição

    Exemplo:
        'Araquari'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome

        location: localização (o2m)

        institutions: instituições localizadas nesse campus (m2m)

        institutions_campus: relação inversa para a model InstitutionCampus
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=CAMPUS_MAX_LENGTH, unique=True)
    location = models.ForeignKey("Location", related_name="campus", on_delete=models.PROTECT)
    institutions = models.ManyToManyField("Institution", related_name="campus", through="InstitutionCampus")

    def __str__(self):
        return self.name


class InstitutionCampus(SafeDeleteModel):
    """
    Define uma instituição pertencente à um campus. É uma associativa entre a model de Institution e Campus

    Exemplo:
        'Instituto Federal Catarinense - Campus Araquari'

    Atributos:
        _safedelete_policy: NO_DELETE

        institution: objeto do tipo model Institution (o2m)

        campus: objeto do tipo model Campus (o2m)

        academic_education: relação inversa para a model AcademicEducationInstitutionCampus
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    institution = models.ForeignKey(
        "Institution",
        related_name="institutions_campus",
        related_query_name="institution_campus",
        on_delete=models.PROTECT,
    )
    campus = models.ForeignKey(
        "Campus",
        related_name="institutions_campus",
        related_query_name="institution_campus",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ["institution", "campus"]

    def __str__(self):
        return f"{self.institution} - {self.campus}"


class AcademicEducationInstitutionCampus(SafeDeleteModel):
    """
    Define uma formação acadêmica que pertence à uma instituição de um campus. É uma associativa entre a model de
    AcademicEducation e InstitutionCampus

    Exemplo:
        'Sistemas de Informação - IFC Araquari'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        academic_education: objeto do tipo model 'AcademicEducation' (o2m)

        institution_campus: objeto do tipo model 'InstitutionCampus' (o2m)

        students: relação inversa para a model Student
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    academic_education = models.ForeignKey(
        "AcademicEducation",
        related_name="institutions_campus",
        related_query_name="institution_campus",
        on_delete=models.CASCADE,
    )
    institution_campus = models.ForeignKey(
        "InstitutionCampus", related_name="academic_education", on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ["institution_campus", "academic_education"]

    def __str__(self):
        return f"{self.academic_education} - {self.institution_campus}"
