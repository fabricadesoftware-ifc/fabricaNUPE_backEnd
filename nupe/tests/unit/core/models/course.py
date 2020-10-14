from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AcademicEducation, Course, Grade


class CourseTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Course, "_safedelete_policy"), True)
        self.assertIs(hasattr(Course, "name"), True)
        self.assertIs(hasattr(Course, "grades"), True)
        self.assertIs(hasattr(Course, "academic_education"), True)

    def test_return_str(self):
        course = baker.prepare(Course)

        self.assertEqual(str(course), course.name)


class GradeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Grade, "_safedelete_policy"), True)
        self.assertIs(hasattr(Grade, "name"), True)
        self.assertIs(hasattr(Grade, "courses"), True)
        self.assertIs(hasattr(Grade, "academic_education"), True)

    def test_return_str(self):
        grade = baker.prepare(Grade)

        self.assertEqual(str(grade), grade.name)


class AcademicEducationTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AcademicEducation, "_safedelete_policy"), True)
        self.assertIs(hasattr(AcademicEducation, "course"), True)
        self.assertIs(hasattr(AcademicEducation, "grade"), True)
        self.assertIs(hasattr(AcademicEducation, "academic_education_campus"), True)

    def test_return_str(self):
        academic_education = baker.prepare(AcademicEducation)

        str_expected = f"{academic_education.grade} em {academic_education.course}"
        self.assertEqual(str(academic_education), str_expected)
