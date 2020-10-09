from rest_framework.serializers import ModelSerializer

from nupe.core.models import AttendanceReason


class AttendanceReasonSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um motivo de atendimento e também
    detalha ou lista informações sobre um ou mais motivos de atendimento

    Campos:
        id: identificador (somente leitura)

        name: nome do motivo de atendimento

        description: descrição do motivo de atendimento

        father_reason: motivo de atendimento pai (auto relacionamento)
    """

    class Meta:
        model = AttendanceReason
        fields = ["id", "name", "description", "father_reason"]
