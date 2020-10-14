from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AttendanceReason


class AttendanceReasonTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AttendanceReason, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReason, "name"), True)
        self.assertIs(hasattr(AttendanceReason, "description"), True)
        self.assertIs(hasattr(AttendanceReason, "father_reason"), True)
        self.assertIs(hasattr(AttendanceReason, "sons_reasons"), True)
        self.assertIs(hasattr(AttendanceReason, "only_father"), True)

    def test_return_str(self):
        attendance_reason = baker.prepare(AttendanceReason)

        str_expected = f"{attendance_reason.name} - {attendance_reason.description}"
        self.assertEqual(str(attendance_reason), str_expected)
