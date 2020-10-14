from django.db import models
from safedelete.models import NO_DELETE, SOFT_DELETE_CASCADE, SafeDeleteModel


class Institution(SafeDeleteModel):
    """
    Define o nome de uma instituição

    Exemplo:
        'Instituto Federal Catarinense'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome

        campus: relação inversa para a model Campus
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Campus(SafeDeleteModel):
    """
    Define informações de um campus

    Exemplo:
        'Instituto Federal Catarinense - Campus Araquari'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome do campus

        cnpj: cnpj do campus

        address: endereço de localização do campus

        number: número de identificação do imóvel

        website: site do campus

        location: objeto do tipo model Location (o2m)

        institution: objeto do tipo model Institution (o2m)

        academic_education_campus: relação inversa para a model AcademicEducationCampus

        workers: relação inversa para a model Account
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)
    address = models.CharField(max_length=75)
    number = models.CharField(max_length=10)
    website = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey("Location", related_name="campus", on_delete=models.PROTECT,)
    institution = models.ForeignKey("Institution", related_name="campus", on_delete=models.PROTECT,)

    def __str__(self) -> str:
        return f"{self.institution} - {self.name}"


class AcademicEducationCampus(SafeDeleteModel):
    """
    Define uma formação acadêmica que pertence à um campus. É uma associativa entre a model de
    AcademicEducation e Campus

    Exemplo:
        'Sistemas de Informação - IFC Araquari'

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
