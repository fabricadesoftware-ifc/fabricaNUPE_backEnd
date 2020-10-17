from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField

from nupe.account.models import Account
from nupe.account.serializers.account import AccountDetailSerializer, AccountListSerializer
from nupe.core.models import AccountAttendance, Attendance
from nupe.core.serializers.student import StudentDetailSerializer, StudentListSerializer


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

    attendants = AccountListSerializer(many=True)
    student = StudentListSerializer()

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
    attendants = AccountDetailSerializer(many=True)
    student = StudentDetailSerializer()

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


class AccountAttendanceSerializer(ModelSerializer):
    """
    Retorna uma lista de informações públicas do atendimento de um usuário

    Campos:
        id: identificador

        public_annotation: anotação pública do atendimento

        account: usuário que realizou o atendimento

        attendance_at: data/hora do atendimento

        updated_at: data/hora da atualização do atendimento
    """

    account = AccountDetailSerializer()

    class Meta:
        model = AccountAttendance
        fields = [
            "id",
            "public_annotation",
            "account",
            "attendance_at",
            "updated_at",
        ]


class MyAccountAttendanceSerializer(ModelSerializer):
    """
    Retorna uma lista de informações sobre os atendimentos do usuário atual

    Campos:
        id: identificador

        public_annotation: anotação pública do atendimento

        private_annotation: anotação particular do atendente

        group_annotation: anotação para outros membros do grupo

        attendance: atendimento realizado

        attendance_at: data/hora do atendimento

        updated_at: data/hora da atualização do atendimento
    """

    attendance = AttendanceDetailSerializer()

    class Meta:
        model = AccountAttendance
        fields = [
            "id",
            "public_annotation",
            "private_annotation",
            "group_annotation",
            "attendance",
            "attendance_at",
            "updated_at",
        ]


class AttendanceReportSerializer(ModelSerializer):
    """
    Retorna uma lista completa de informações sobre os atendimentos

    Campos:
        id: identificador

        attendance_reason: motivo do atendimento

        attendance_severity: gravidade do atendimento

        student: informações sobre o aluno

        account_attendance: informações adicionais do atendimento

        status: status do atendimento

        opened_at: data/hora da abertura do atendimento

        closed_at: data/hora do fechamento do atendimento
    """

    attendance_reason = CharField()
    student = StudentDetailSerializer()
    account_attendance = AccountAttendanceSerializer(source="account_attendances", many=True)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "attendance_reason",
            "attendance_severity",
            "student",
            "account_attendance",
            "status",
            "opened_at",
            "closed_at",
        ]
