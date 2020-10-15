from django.db import models
from safedelete.models import NO_DELETE, SafeDeleteModel


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
