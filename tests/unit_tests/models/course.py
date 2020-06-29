from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AcademicEducation, Course, Grade
from resources.const.datas.course import COURSE_NAME, GRADE_NAME


class CourseTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Course, "_safedelete_policy"), True)
        self.assertIs(hasattr(Course, "name"), True)

    def test_return_str(self):
        course = baker.prepare(Course, name=COURSE_NAME)

        self.assertEqual(str(course), course.name)


class GradeTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Grade, "_safedelete_policy"), True)
        self.assertIs(hasattr(Grade, "name"), True)
        self.assertIs(hasattr(Grade, "courses"), True)

    def test_return_str(self):
        grade = baker.prepare(Grade, name=GRADE_NAME)

        self.assertEqual(str(grade), grade.name)


class AcademicEducationTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AcademicEducation, "_safedelete_policy"), True)
        self.assertIs(hasattr(AcademicEducation, "course"), True)
        self.assertIs(hasattr(AcademicEducation, "grade"), True)

    def test_return_str(self):
        academic_education = baker.prepare(AcademicEducation)

        str_expected = f"{academic_education.grade} em {academic_education.course}"
        self.assertEqual(str(academic_education), str_expected)
