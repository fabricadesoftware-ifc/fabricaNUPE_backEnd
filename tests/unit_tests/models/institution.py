from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AcademicEducationCampus, Campus, Institution, InstitutionCampus


class InstitutionTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Institution, "_safedelete_policy"), True)
        self.assertIs(hasattr(Institution, "name"), True)

    def test_return_str(self):
        institution = baker.prepare(Institution)

        self.assertEqual(str(institution), institution.name)


class CampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Campus, "_safedelete_policy"), True)
        self.assertIs(hasattr(Campus, "name"), True)
        self.assertIs(hasattr(Campus, "location"), True)
        self.assertIs(hasattr(Campus, "institutions"), True)
        self.assertIs(hasattr(Campus, "academic_education"), True)

    def test_return_str(self):
        campus = baker.prepare(Campus)

        self.assertEqual(str(campus), campus.name)


class InstitutionCampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(InstitutionCampus, "_safedelete_policy"), True)
        self.assertIs(hasattr(InstitutionCampus, "institution"), True)
        self.assertIs(hasattr(InstitutionCampus, "campus"), True)

    def test_return_str(self):
        institution_campus = baker.prepare(InstitutionCampus)

        str_expected = f"{institution_campus.institution} - {institution_campus.campus}"
        self.assertEqual(str(institution_campus), str_expected)


class AcademicEducationCampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AcademicEducationCampus, "_safedelete_policy"), True)
        self.assertIs(hasattr(AcademicEducationCampus, "academic_education"), True)
        self.assertIs(hasattr(AcademicEducationCampus, "campus"), True)

    def test_return_str(self):
        academic_education_campus = baker.prepare(AcademicEducationCampus)

        str_expected = f"{academic_education_campus.academic_education} - {academic_education_campus.campus}"
        self.assertEqual(str(academic_education_campus), str_expected)
