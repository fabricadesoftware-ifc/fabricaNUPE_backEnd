from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AccountAttendance, Attendance


class AttendanceTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Attendance, "_safedelete_policy"), True)
        self.assertIs(hasattr(Attendance, "attendance_reason"), True)
        self.assertIs(hasattr(Attendance, "attendance_severity"), True)
        self.assertIs(hasattr(Attendance, "attendants"), True)
        self.assertIs(hasattr(Attendance, "student"), True)
        self.assertIs(hasattr(Attendance, "status"), True)
        self.assertIs(hasattr(Attendance, "opened_at"), True)
        self.assertIs(hasattr(Attendance, "closed_at"), True)

    def test_return_str(self):
        attendance = baker.prepare(Attendance)

        str_expected = f"""
        {attendance.student},
        Gravidade: {attendance.attendance_severity},
        Descrição: {attendance.attendance_reason.description or 'Nenhuma'}
        """
        self.assertEqual(str(attendance), str_expected)


class AccountAttendanceTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AccountAttendance, "_safedelete_policy"), True)
        self.assertIs(hasattr(AccountAttendance, "public_annotation"), True)
        self.assertIs(hasattr(AccountAttendance, "private_annotation"), True)
        self.assertIs(hasattr(AccountAttendance, "group_annotation"), True)
        self.assertIs(hasattr(AccountAttendance, "attendance"), True)
        self.assertIs(hasattr(AccountAttendance, "account"), True)
        self.assertIs(hasattr(AccountAttendance, "attendance_at"), True)
        self.assertIs(hasattr(AccountAttendance, "updated_at"), True)

    def test_return_str(self):
        account_attendance = baker.prepare(AccountAttendance)

        str_expected = (
            f"Atendente: {account_attendance.account.full_name}, Anotação: {account_attendance.public_annotation}"
        )
        self.assertEqual(str(account_attendance), str_expected)
