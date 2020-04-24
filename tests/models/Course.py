from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import COURSE_MAX_LENGTH, GRADE_MAX_LENGTH, AcademicEducation, Course, Grade

COURSE_NAME = "Informática"
GRADE_NAME = "Técnico"


class CourseTestCase(TestCase):
    def test_create_valid(self):
        course = Course.objects.create(name=COURSE_NAME)
        self.assertEqual(course.name, COURSE_NAME)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Course.objects.create(name=COURSE_NAME * COURSE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Course.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Course.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            Course.objects.create(name=COURSE_NAME)
            Course.objects.create(name=COURSE_NAME)


class GradeTestCase(TestCase):
    def test_create_valid(self):
        grade = Grade.objects.create(name=GRADE_NAME)
        self.assertEqual(grade.name, GRADE_NAME)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name=GRADE_NAME * GRADE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Grade.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name="").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            Grade.objects.create(name=GRADE_NAME)
            Grade.objects.create(name=GRADE_NAME)


class AcademicEducationTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name=COURSE_NAME)
        Grade.objects.create(name=GRADE_NAME)

    def test_create_valid(self):
        course = Course.objects.all().first()
        grade = Grade.objects.all().first()

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        self.assertEqual(academic_education.course.name, COURSE_NAME)
        self.assertEqual(academic_education.grade.name, GRADE_NAME)
        self.assertEqual(AcademicEducation.objects.all().count(), 1)

    def test_create_invalid_null(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                AcademicEducation.objects.create(course=None)

        with self.assertRaises(IntegrityError):
            AcademicEducation.objects.create(grade=None)

    def test_create_invalid_blank(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                AcademicEducation.objects.create(course="")

        with self.assertRaises(ValueError):
            AcademicEducation.objects.create(grade="")

    def test_create_invalid_course_and_grade_instance(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                AcademicEducation.objects.create(course=1)

        with self.assertRaises(ValueError):
            AcademicEducation.objects.create(grade=1)

    def test_create_invalid_course_and_grade_unique_together(self):
        course = Course.objects.all().first()
        grade = Grade.objects.all().first()

        with self.assertRaises(IntegrityError):
            AcademicEducation.objects.create(course=course, grade=grade)
            AcademicEducation.objects.create(course=course, grade=grade)
