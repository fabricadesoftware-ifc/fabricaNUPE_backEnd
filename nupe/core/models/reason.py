from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class SpecialNeedType(SafeDeleteModel):
    """
    Define os tipos de necessidades especiais de um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class CrisisType(SafeDeleteModel):
    """
    Define os tipos de crises de um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class DrugType(SafeDeleteModel):
    """
    Define os tipos de drogas utilizadas por um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class AttendanceReason(SafeDeleteModel):
    """
    Define o motivo do atendimento estar ocorrendo

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        description: descrição

        special_need: necessidade especial sendo atendida

        crisis: crise sendo atendida

        drug: tipo de droga utilizada pelo aluno
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    description = models.TextField(max_length=255)
    special_need = models.ForeignKey(
        SpecialNeedType, related_name="attendances", related_query_name="attendance", on_delete=models.CASCADE
    )
    crisis = models.ForeignKey(
        CrisisType, related_name="attendances", related_query_name="attendance", on_delete=models.CASCADE
    )
    drug = models.ForeignKey(
        DrugType, related_name="attendances", related_query_name="attendance", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.description
