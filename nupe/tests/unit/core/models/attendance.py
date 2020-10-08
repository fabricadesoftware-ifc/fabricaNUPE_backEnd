from django.test import TestCase
from model_bakery import baker

from nupe.core.models import Attendance


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

        str_expected = (
            f"{attendance.student} - {attendance.attendance_severity} - {attendance.attendance_reason.description}"
        )
        self.assertEqual(str(attendance), str_expected)
