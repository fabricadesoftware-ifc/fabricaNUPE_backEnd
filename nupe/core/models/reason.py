from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteManager, SafeDeleteModel


class AttendanceReasonManager(SafeDeleteManager):
    def get_queryset(self):
        return super().get_queryset().filter(father_reason=None)


class AttendanceReason(SafeDeleteModel):
    """
    Define o motivo do atendimento estar ocorrendo

    Atributos:
        _safedelete_policy = SOFT_DELETE_CASCADE

        name: nome do motivo

        description: descrição do motivo

        father_reason: motivo de atendimento pai (auto relacionamento)

        sons_reasons: relação inversa para o objeto da model AttendanceReason
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    father_reason = models.ForeignKey(
        "core.AttendanceReason",
        related_name="sons_reasons",
        related_query_name="son_reason",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )

    only_father = AttendanceReasonManager()

    def __str__(self) -> str:
        return self.description
