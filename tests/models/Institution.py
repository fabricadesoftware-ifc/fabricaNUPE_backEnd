from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from nupe.core.models import (
    CAMPUS_MAX_LENGTH,
    INSTITUTION_MAX_LENGTH,
    AcademicEducation,
    AcademicEducationCampus,
    Campus,
    City,
    Course,
    Grade,
    Institution,
    InstitutionCampus,
    Location,
    State,
)
from tests.models.Course import COURSE_NAME, GRADE_NAME
from tests.models.Location import CITY_NAME, STATE_NAME

INSTITUTION_NAME = "Instituto Federal Catarinense"
CAMPUS_NAME = "Araquari"


class InstitutionTestCase(TestCase):
    def test_create_valid(self):
        institution = Institution.objects.create(name=INSTITUTION_NAME)
        self.assertEqual(institution.name, INSTITUTION_NAME)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Institution.objects.create(name=INSTITUTION_NAME * INSTITUTION_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Institution.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Institution.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            Institution.objects.create(name=INSTITUTION_NAME)
            Institution.objects.create(name=INSTITUTION_NAME)


class CampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        Location.objects.create(city=city, state=state)

    def test_create_valid(self):
        location = Location.objects.all().first()

        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)
        self.assertEqual(campus.name, CAMPUS_NAME)

    def test_create_invalid_max_length(self):
        location = Location.objects.all().first()

        with self.assertRaises(ValidationError):
            Campus.objects.create(name=CAMPUS_NAME * CAMPUS_MAX_LENGTH, location=location).clean_fields()

    def test_create_invalid_name_null(self):
        with self.assertRaises(IntegrityError):
            Campus.objects.create(name=None)

    def test_create_invalid_location_null(self):
        with self.assertRaises(IntegrityError):
            Campus.objects.create(location=None)

    def test_create_invalid_blank(self):
        location = Location.objects.all().first()

        with self.assertRaises(ValidationError):
            Campus.objects.create(location=location).clean_fields()

    def test_create_invalid_unique_name(self):
        location = Location.objects.all().first()

        with self.assertRaises(IntegrityError):
            Campus.objects.create(name=CAMPUS_NAME, location=location)
            Campus.objects.create(name=CAMPUS_NAME, location=location)


class InstitutionCampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        Location.objects.create(city=city, state=state)

    def test_create_valid(self):
        location = Location.objects.all().first()

        institution = Institution.objects.create(name=INSTITUTION_NAME)
        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)
        InstitutionCampus.objects.create(institution=institution, campus=campus)

    def test_create_invalid_null(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                InstitutionCampus.objects.create(institution=None)

        with self.assertRaises(IntegrityError):
            InstitutionCampus.objects.create(campus=None)

    def test_create_invalid_blank(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                InstitutionCampus.objects.create(institution="")

        with self.assertRaises(ValueError):
            InstitutionCampus.objects.create(campus="")

    def test_create_invalid_course_and_grade_instance(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                InstitutionCampus.objects.create(institution=1)

        with self.assertRaises(ValueError):
            InstitutionCampus.objects.create(campus=1)

    def test_create_invalid_course_and_grade_unique_together(self):
        institution = Course.objects.all().first()
        campus = Campus.objects.all().first()

        with self.assertRaises(IntegrityError):
            InstitutionCampus.objects.create(institution=institution, campus=campus)
            InstitutionCampus.objects.create(institution=institution, campus=campus)


class AcademicEducationCampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        Location.objects.create(city=city, state=state)

        course = Course.objects.create(name=COURSE_NAME)
        grade = Grade.objects.create(name=GRADE_NAME)
        AcademicEducation.objects.create(course=course, grade=grade)

    def test_create_valid(self):
        location = Location.objects.all().first()
        academic_education = AcademicEducation.objects.all().first()

        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)
        AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)

    def test_create_invalid_null(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                AcademicEducationCampus.objects.create(academic_education=None)

        with self.assertRaises(IntegrityError):
            AcademicEducationCampus.objects.create(campus=None)

    def test_create_invalid_blank(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                AcademicEducationCampus.objects.create(academic_education="")

        with self.assertRaises(ValueError):
            AcademicEducationCampus.objects.create(campus="")

    def test_create_invalid_course_and_grade_instance(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                AcademicEducationCampus.objects.create(academic_education=1)

        with self.assertRaises(ValueError):
            AcademicEducationCampus.objects.create(campus=1)

    def test_create_invalid_course_and_grade_unique_together(self):
        academic_education = AcademicEducation.objects.all().first()
        campus = Campus.objects.all().first()

        with self.assertRaises(IntegrityError):
            AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
            AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
