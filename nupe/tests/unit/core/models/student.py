from django.test import TestCase
from model_bakery import baker

from nupe.core.models import Responsible, Student


class StudentTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Student, "_safedelete_policy"), True)
        self.assertIs(hasattr(Student, "_academic_education_campus_deleted_id"), True)
        self.assertIs(hasattr(Student, "registration"), True)
        self.assertIs(hasattr(Student, "person"), True)
        self.assertIs(hasattr(Student, "academic_education_campus"), True)
        self.assertIs(hasattr(Student, "responsibles_persons"), True)
        self.assertIs(hasattr(Student, "graduated"), True)
        self.assertIs(hasattr(Student, "ingress_date"), True)
        self.assertIs(hasattr(Student, "updated_at"), True)
        self.assertIs(hasattr(Student, "responsibles"), True)

    def test_return_str(self):
        student = baker.prepare(Student)

        str_expected = f"{student.person} - {student.registration}"
        self.assertEqual(str(student), str_expected)

    def test_return_properties(self):
        academic_education_campus = baker.prepare("core.AcademicEducationCampus")
        student = baker.prepare(Student, academic_education_campus=academic_education_campus)

        self.assertEqual(student.age, student.person.age)
        self.assertEqual(student.academic_education, str(student.academic_education_campus.academic_education))


class ResponsibleTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Responsible, "_safedelete_policy"), True)
        self.assertIs(hasattr(Responsible, "student"), True)
        self.assertIs(hasattr(Responsible, "person"), True)

    def test_return_str(self):
        responsible = baker.prepare(Responsible)

        str_expected = f"{responsible.person} responsável de {responsible.student.person}"
        self.assertEqual(str(responsible), str_expected)
