from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AcademicEducationCampus, Campus, Institution, Student


class InstitutionTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Institution, "_safedelete_policy"), True)
        self.assertIs(hasattr(Institution, "name"), True)
        self.assertIs(hasattr(Institution, "campus"), True)

    def test_return_str(self):
        institution = baker.prepare(Institution)

        self.assertEqual(str(institution), institution.name)


class CampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Campus, "_safedelete_policy"), True)
        self.assertIs(hasattr(Campus, "name"), True)
        self.assertIs(hasattr(Campus, "cnpj"), True)
        self.assertIs(hasattr(Campus, "address"), True)
        self.assertIs(hasattr(Campus, "number"), True)
        self.assertIs(hasattr(Campus, "website"), True)
        self.assertIs(hasattr(Campus, "location"), True)
        self.assertIs(hasattr(Campus, "institution"), True)
        self.assertIs(hasattr(Campus, "academic_education_campus"), True)
        self.assertIs(hasattr(Campus, "workers"), True)

    def test_return_str(self):
        campus = baker.prepare(Campus)

        str_expected = f"{campus.institution} - {campus.name}"
        self.assertEqual(str(campus), str_expected)


class AcademicEducationCampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AcademicEducationCampus, "_safedelete_policy"), True)
        self.assertIs(hasattr(AcademicEducationCampus, "academic_education"), True)
        self.assertIs(hasattr(AcademicEducationCampus, "campus"), True)
        self.assertIs(hasattr(AcademicEducationCampus, "students"), True)

    def test_return_str(self):
        academic_education_campus = baker.prepare(AcademicEducationCampus)

        str_expected = f"""{academic_education_campus.academic_education} - {
            academic_education_campus.campus
            }"""
        self.assertEqual(str(academic_education_campus), str_expected)

    # custom signals
    def test_signals_pre_delete_should_set_related_as_none(self):
        academic_education_campus = baker.make(AcademicEducationCampus)
        student = baker.make(Student, academic_education_campus=academic_education_campus)

        academic_education_campus.delete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNone(student.academic_education_campus)

    def test_signals_post_delete_should_restore_related(self):
        academic_education_campus = baker.make(AcademicEducationCampus)
        student = baker.make(Student, academic_education_campus=academic_education_campus)

        academic_education_campus.delete()
        academic_education_campus.undelete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNotNone(student.academic_education_campus)
        self.assertEqual(student.academic_education_campus, academic_education_campus)

    def test_signals_post_delete_not_should_restore(self):
        academic_education_campus1 = baker.make(AcademicEducationCampus)
        academic_education_campus2 = baker.make(AcademicEducationCampus)
        student = baker.make(Student, academic_education_campus=academic_education_campus1)

        academic_education_campus1.delete()
        academic_education_campus2.delete()

        academic_education_campus2.undelete()

        student = Student.objects.get(pk=student.id)
        self.assertIsNone(student.academic_education_campus)
