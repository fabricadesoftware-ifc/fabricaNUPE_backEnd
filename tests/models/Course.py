from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import COURSE_MAX_LENGTH, GRADE_MAX_LENGTH, AcademicEducation, Course, Grade

course_name = "Informática"
grade_name = "Técnico"


class CourseTestCase(TestCase):
    def test_create_valid(self):
        course = Course.objects.create(name=course_name)
        self.assertEqual(course.name, course_name)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Course.objects.create(name=course_name * COURSE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Course.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Course.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            Course.objects.create(name=course_name)
            Course.objects.create(name=course_name)


class GradeTestCase(TestCase):
    def test_create_valid(self):
        grade = Grade.objects.create(name=grade_name)
        self.assertEqual(grade.name, grade_name)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name=grade_name * GRADE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Grade.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name="").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            Grade.objects.create(name=grade_name)
            Grade.objects.create(name=grade_name)


class AcademicEducationTestCase(TestCase):
    def test_create_valid(self):
        course = Course.objects.create(name=course_name)
        grade = Grade.objects.create(name=grade_name)

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        self.assertEqual(academic_education.course.name, course_name)
        self.assertEqual(academic_education.grade.name, grade_name)
        self.assertEqual(AcademicEducation.objects.all().count(), 1)

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            AcademicEducation.objects.create()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValueError):
            AcademicEducation.objects.create(course="", grade="")

    def test_create_invalid_course_and_grade_instance(self):
        with self.assertRaises(ValueError):
            AcademicEducation.objects.create(course=1, grade=1)

    def test_create_invalid_course_and_grade_unique_together(self):
        course = Course.objects.create(name=course_name)
        grade = Grade.objects.create(name=grade_name)

        with self.assertRaises(IntegrityError):
            AcademicEducation.objects.create(course=course, grade=grade)
            AcademicEducation.objects.create(course=course, grade=grade)
