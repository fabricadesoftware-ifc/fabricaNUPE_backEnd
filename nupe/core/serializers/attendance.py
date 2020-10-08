from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, StringRelatedField

from nupe.account.models.account import Account
from nupe.core.models import Attendance


class AttendanceCreateSerializer(ModelSerializer):
    """
    Recebe e valida as informações para então cadastrar ou atualizar um atendimento

    Campos:
        id: identificador (somente leitura)

        attendance_reason: identificador do objeto da model AttendanceReason

        attendance_severity: char que representa a gravidade do atendimento. Escolhas disponíveis na documentação
        da model Attendance

        attendants: identificadores do objeto da model Account

        student: identificador do objeto da model Student

        status: char que representa o status do atendimento. Escolhas disponíveis na documentação
        da model Attendance
    """

    attendants = PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendance_reason",
            "attendance_severity",
            "attendants",
            "student",
            "status",
        ]


class AttendanceListSerializer(ModelSerializer):
    """
    Retorna uma lista de atendimentos cadastrados no banco de dados

    Campos:
        id: identificador (somente leitura)

        attendants: identificadores do objeto da model Account

        student: identificador do objeto da model Student

        status: char que representa o status do atendimento. Escolhas disponíveis na documentação
        da model Attendance
    """

    attendants = StringRelatedField(many=True)
    student = CharField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendants",
            "student",
            "status",
        ]


class AttendanceDetailSerializer(ModelSerializer):
    """
    Retorna os detalhes de um atendimento específico

    Campos:
        id: identificador (somente leitura)

        attendance_reason: identificador do objeto da model AttendanceReason

        attendance_severity: char que representa a gravidade do atendimento. Escolhas disponíveis na documentação
        da model Attendance

        attendants: identificadores do objeto da model Account

        student: identificador do objeto da model Student

        status: char que representa o status do atendimento. Escolhas disponíveis na documentação
        da model Attendance

        opened_at: data de abertura do atendimento

        closed_at: data de fechamento do atendimento
    """

    attendance_reason = CharField()
    attendants = StringRelatedField(many=True)
    student = CharField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendance_reason",
            "attendance_severity",
            "attendants",
            "student",
            "status",
            "opened_at",
            "closed_at",
        ]
