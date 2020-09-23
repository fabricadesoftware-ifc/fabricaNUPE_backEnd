from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AcademicEducationInstitutionCampus, Campus, Institution, InstitutionCampus, Student


class InstitutionTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Institution, "_safedelete_policy"), True)
        self.assertIs(hasattr(Institution, "name"), True)
        self.assertIs(hasattr(Institution, "campus"), True)
        self.assertIs(hasattr(Institution, "institutions_campus"), True)

    def test_return_str(self):
        institution = baker.prepare(Institution)

        self.assertEqual(str(institution), institution.name)


class CampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Campus, "_safedelete_policy"), True)
        self.assertIs(hasattr(Campus, "name"), True)
        self.assertIs(hasattr(Campus, "location"), True)
        self.assertIs(hasattr(Campus, "institutions"), True)
        self.assertIs(hasattr(Campus, "institutions_campus"), True)

    def test_return_str(self):
        campus = baker.prepare(Campus)

        self.assertEqual(str(campus), campus.name)


class InstitutionCampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(InstitutionCampus, "_safedelete_policy"), True)
        self.assertIs(hasattr(InstitutionCampus, "institution"), True)
        self.assertIs(hasattr(InstitutionCampus, "campus"), True)
        self.assertIs(hasattr(InstitutionCampus, "academic_education"), True)

    def test_return_str(self):
        institution_campus = baker.prepare(InstitutionCampus)

        str_expected = f"{institution_campus.institution} - {institution_campus.campus}"
        self.assertEqual(str(institution_campus), str_expected)


class AcademicEducationInstitutionCampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AcademicEducationInstitutionCampus, "_safedelete_policy"), True)
        self.assertIs(hasattr(AcademicEducationInstitutionCampus, "academic_education"), True)
        self.assertIs(hasattr(AcademicEducationInstitutionCampus, "institution_campus"), True)
        self.assertIs(hasattr(AcademicEducationInstitutionCampus, "students"), True)

    def test_return_str(self):
        academic_education_institution_campus = baker.prepare(AcademicEducationInstitutionCampus)

        str_expected = f"""{academic_education_institution_campus.academic_education} - {
            academic_education_institution_campus.institution_campus
            }"""
        self.assertEqual(str(academic_education_institution_campus), str_expected)

    # custom signals
    def test_signals_pre_delete_should_set_related_as_none(self):
        academic_education_institution_campus = baker.make(AcademicEducationInstitutionCampus)
        student = baker.make(Student, academic_education_institution_campus=academic_education_institution_campus)

        academic_education_institution_campus.delete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNone(student.academic_education_institution_campus)

    def test_signals_post_delete_should_restore_related(self):
        academic_education_institution_campus = baker.make(AcademicEducationInstitutionCampus)
        student = baker.make(Student, academic_education_institution_campus=academic_education_institution_campus)

        academic_education_institution_campus.delete()
        academic_education_institution_campus.undelete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNotNone(student.academic_education_institution_campus)
        self.assertEqual(student.academic_education_institution_campus, academic_education_institution_campus)

    def test_signals_post_delete_not_should_restore(self):
        academic_education_institution_campus1 = baker.make(AcademicEducationInstitutionCampus)
        academic_education_institution_campus2 = baker.make(AcademicEducationInstitutionCampus)
        student = baker.make(Student, academic_education_institution_campus=academic_education_institution_campus1)

        academic_education_institution_campus1.delete()
        academic_education_institution_campus2.delete()

        academic_education_institution_campus2.undelete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNone(student.academic_education_institution_campus)
