from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AttendanceReason, CrisisType, DrugType, SpecialNeedType


class SpecialNeedTypeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(SpecialNeedType, "_safedelete_policy"), True)
        self.assertIs(hasattr(SpecialNeedType, "name"), True)
        self.assertIs(hasattr(SpecialNeedType, "description"), True)
        self.assertIs(hasattr(SpecialNeedType, "attendances"), True)

    def test_return_str(self):
        special_need_type = baker.prepare(SpecialNeedType)

        self.assertEqual(str(special_need_type), special_need_type.name)


class CrisisTypeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(SpecialNeedType, "_safedelete_policy"), True)
        self.assertIs(hasattr(CrisisType, "name"), True)
        self.assertIs(hasattr(CrisisType, "description"), True)
        self.assertIs(hasattr(CrisisType, "attendances"), True)

    def test_return_str(self):
        crisis_type = baker.prepare(CrisisType)

        self.assertEqual(str(crisis_type), crisis_type.name)


class DrugTypeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(SpecialNeedType, "_safedelete_policy"), True)
        self.assertIs(hasattr(DrugType, "name"), True)
        self.assertIs(hasattr(DrugType, "description"), True)
        self.assertIs(hasattr(DrugType, "attendances"), True)

    def test_return_str(self):
        drug_type = baker.prepare(DrugType)

        self.assertEqual(str(drug_type), drug_type.name)


class AttendanceReasonTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(SpecialNeedType, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReason, "description"), True)
        self.assertIs(hasattr(AttendanceReason, "special_need"), True)
        self.assertIs(hasattr(AttendanceReason, "crisis"), True)
        self.assertIs(hasattr(AttendanceReason, "drug"), True)

    def test_return_str(self):
        attendance_reason = baker.prepare(AttendanceReason)

        self.assertEqual(str(attendance_reason), attendance_reason.description)
