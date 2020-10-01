from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class Function(SafeDeleteModel):
    """
    Define os tipos de funcionários

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome da função

        description: descrição da função, o que faz etc.

        workers: relação inversa para a model Account
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Sector(SafeDeleteModel):
    """
    Define os tipos de setores

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome do setor

        description: descrição do setor

        workers: relação inversa para a model Account
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name
