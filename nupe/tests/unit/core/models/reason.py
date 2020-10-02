from django.test import TestCase
from model_bakery import baker

from nupe.core.models import (
    AttendanceReason,
    AttendanceReasonCrisis,
    AttendanceReasonDrug,
    AttendanceReasonSpecialNeed,
    CrisisType,
    DrugType,
    SpecialNeedType,
)


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
        self.assertIs(hasattr(CrisisType, "_safedelete_policy"), True)
        self.assertIs(hasattr(CrisisType, "name"), True)
        self.assertIs(hasattr(CrisisType, "description"), True)
        self.assertIs(hasattr(CrisisType, "attendances"), True)

    def test_return_str(self):
        crisis_type = baker.prepare(CrisisType)

        self.assertEqual(str(crisis_type), crisis_type.name)


class DrugTypeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(DrugType, "_safedelete_policy"), True)
        self.assertIs(hasattr(DrugType, "name"), True)
        self.assertIs(hasattr(DrugType, "description"), True)
        self.assertIs(hasattr(DrugType, "attendances"), True)

    def test_return_str(self):
        drug_type = baker.prepare(DrugType)

        self.assertEqual(str(drug_type), drug_type.name)


class AttendanceReasonTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AttendanceReason, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReason, "description"), True)
        self.assertIs(hasattr(AttendanceReason, "special_need"), True)
        self.assertIs(hasattr(AttendanceReason, "crisis"), True)
        self.assertIs(hasattr(AttendanceReason, "drug"), True)

    def test_return_str(self):
        attendance_reason = baker.prepare(AttendanceReason)

        self.assertEqual(str(attendance_reason), attendance_reason.description)


class AttendanceReasonSpecialNeedTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AttendanceReasonSpecialNeed, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReasonSpecialNeed, "attendance_reason"), True)
        self.assertIs(hasattr(AttendanceReasonSpecialNeed, "special_need"), True)

    def test_return_str(self):
        attendance_reason_special_need = baker.prepare(AttendanceReasonSpecialNeed)

        str_expected = (
            f"{attendance_reason_special_need.attendance_reason} - {attendance_reason_special_need.special_need}"
        )
        self.assertEqual(str(attendance_reason_special_need), str_expected)


class AttendanceReasonCrisisTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AttendanceReasonCrisis, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReasonCrisis, "attendance_reason"), True)
        self.assertIs(hasattr(AttendanceReasonCrisis, "crisis"), True)

    def test_return_str(self):
        attendance_reason_crisis = baker.prepare(AttendanceReasonCrisis)

        str_expected = f"{attendance_reason_crisis.attendance_reason} - {attendance_reason_crisis.crisis}"
        self.assertEqual(str(attendance_reason_crisis), str_expected)


class AttendanceReasonDrugTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AttendanceReasonDrug, "_safedelete_policy"), True)
        self.assertIs(hasattr(AttendanceReasonDrug, "attendance_reason"), True)
        self.assertIs(hasattr(AttendanceReasonDrug, "drug"), True)

    def test_return_str(self):
        attendance_reason_drug = baker.prepare(AttendanceReasonDrug)

        str_expected = f"{attendance_reason_drug.attendance_reason} - {attendance_reason_drug.drug}"
        self.assertEqual(str(attendance_reason_drug), str_expected)
