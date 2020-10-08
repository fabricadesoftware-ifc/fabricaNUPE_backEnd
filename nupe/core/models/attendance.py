from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class Attendance(SafeDeleteModel):
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"
    SERIOUS = "S"

    ATTENDANCE_SEVERITY_CHOICES = [
        (LOW, "Baixa"),
        (MEDIUM, "Média"),
        (HIGH, "Alta"),
        (SERIOUS, "Grave"),
    ]

    OPEN = "O"
    ON_HOLD = "OH"
    IN_PROGRESS = "IP"
    CLOSED = "C"

    STATUS_CHOICES = [
        (OPEN, "Aberto"),
        (ON_HOLD, "Em espera"),
        (IN_PROGRESS, "Em Atendimento"),
        (CLOSED, "Fechado"),
    ]

    _safedelete_policy = SOFT_DELETE_CASCADE

    attendance_reason = models.ForeignKey(
        "core.AttendanceReason", related_name="attendances", related_query_name="attendance", on_delete=models.CASCADE
    )
    attendance_severity = models.CharField(max_length=1, choices=ATTENDANCE_SEVERITY_CHOICES)
    attendants = models.ManyToManyField(
        "account.Account", related_name="attendances", related_query_name="attendance", through="AccountAttendance"
    )
    student = models.ForeignKey(
        "core.Student", related_name="consultations", related_query_name="consultation", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPEN)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"{self.student} - {self.attendance_severity} - {self.attendance_reason.description}"


class AccountAttendance(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    annotation = models.TextField(max_length="255")
    attendance = models.ForeignKey(
        "core.Attendance",
        related_name="account_attendances",
        related_query_name="account_attendance",
        on_delete=models.CASCADE,
    )
    account = models.ForeignKey(
        "account.Account",
        related_name="account_attendances",
        related_query_name="account_attendance",
        on_delete=models.CASCADE,
    )
    attendance_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
