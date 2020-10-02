from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class SpecialNeedType(SafeDeleteModel):
    """
    Define os tipos de necessidades especiais de um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição

        attendances: relação inversa para a model AttendanceReason
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class CrisisType(SafeDeleteModel):
    """
    Define os tipos de crises de um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição

        attendances: relação inversa para a model AttendanceReason
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class DrugType(SafeDeleteModel):
    """
    Define os tipos de drogas utilizadas por um aluno que será atendido

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome

        description: descrição

        attendances: relação inversa para a model AttendanceReason
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class AttendanceReason(SafeDeleteModel):
    """
    Define o motivo do atendimento estar ocorrendo

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        description: descrição

        special_need: necessidades especiais sendo atendida

        crisis: crises sendo atendida

        drug: tipos de drogas utilizadas pelo aluno
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    description = models.TextField(max_length=255)
    special_need = models.ManyToManyField(
        SpecialNeedType,
        related_name="attendances",
        related_query_name="attendance",
        through="AttendanceReasonSpecialNeed",
    )
    crisis = models.ManyToManyField(
        CrisisType, related_name="attendances", related_query_name="attendance", through="AttendanceReasonCrisis"
    )
    drug = models.ManyToManyField(
        DrugType, related_name="attendances", related_query_name="attendance", through="AttendanceReasonDrug"
    )

    def __str__(self) -> str:
        return self.description


class AttendanceReasonSpecialNeed(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    attendance_reason = models.ForeignKey(AttendanceReason, on_delete=models.CASCADE)
    special_need = models.ForeignKey(SpecialNeedType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.attendance_reason} - {self.special_need}"


class AttendanceReasonCrisis(SafeDeleteModel):
    __safedelete_policy = SOFT_DELETE_CASCADE

    attendance_reason = models.ForeignKey(AttendanceReason, on_delete=models.CASCADE)
    crisis = models.ForeignKey(CrisisType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.attendance_reason} - {self.crisis}"


class AttendanceReasonDrug(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    attendance_reason = models.ForeignKey(AttendanceReason, on_delete=models.CASCADE)
    drug = models.ForeignKey(DrugType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.attendance_reason} - {self.drug}"
