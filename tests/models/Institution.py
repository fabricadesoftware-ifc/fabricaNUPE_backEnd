from django.core.exceptions import ValidationError
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

        self.assertNotEqual(institution.id, None)
        self.assertEqual(institution.name, INSTITUTION_NAME)
        self.assertEqual(Institution.objects.all().count(), 1)
        self.assertEqual(institution.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Institution(name=INSTITUTION_NAME * INSTITUTION_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Institution(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Institution().clean_fields()

        with self.assertRaises(ValidationError):
            Institution(name="").clean_fields()

        with self.assertRaises(ValidationError):
            Institution(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            Institution.objects.create(name=INSTITUTION_NAME)
            Institution(name=INSTITUTION_NAME).validate_unique()


class CampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        Location.objects.create(city=city, state=state)

    def test_create_valid(self):
        location = Location.objects.all().first()

        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)

        self.assertNotEqual(campus.id, None)
        self.assertEqual(campus.name, CAMPUS_NAME)
        self.assertEqual(campus.location, location)
        self.assertEqual(Campus.objects.all().count(), 1)
        self.assertEqual(campus.full_clean(), None)

    def test_create_invalid_max_length(self):
        location = Location.objects.all().first()

        with self.assertRaises(ValidationError):
            Campus(name=CAMPUS_NAME * CAMPUS_MAX_LENGTH, location=location).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Campus(name=None).clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=None).clean_fields()

    def test_create_invalid_blank(self):
        location = Location.objects.all().first()

        with self.assertRaises(ValidationError):
            Campus().clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=location, name="").clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=location, name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        location = Location.objects.all().first()

        with self.assertRaises(ValidationError):
            Campus.objects.create(name=CAMPUS_NAME, location=location)
            Campus(name=CAMPUS_NAME, location=location).validate_unique()


class InstitutionCampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        location = Location.objects.create(city=city, state=state)

        Institution.objects.create(name=INSTITUTION_NAME)
        Campus.objects.create(name=CAMPUS_NAME, location=location)

    def test_create_valid(self):
        institution = Institution.objects.all().first()
        campus = Campus.objects.all().first()

        institution_campus = InstitutionCampus.objects.create(institution=institution, campus=campus)

        self.assertNotEqual(institution_campus.id, None)
        self.assertEqual(institution_campus.institution, institution)
        self.assertEqual(institution_campus.campus, campus)
        self.assertEqual(InstitutionCampus.objects.all().count(), 1)
        self.assertEqual(institution_campus.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            InstitutionCampus(institution=None).clean_fields()

        with self.assertRaises(ValidationError):
            InstitutionCampus(campus=None).clean_fields()

    def test_create_invalid_course_and_grade_instance(self):
        with self.assertRaises(ValueError):
            InstitutionCampus(institution="").clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(campus="").clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(institution=1).clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(campus=1).clean_fields()

    def test_create_invalid_course_and_grade_unique_together(self):
        institution = Institution.objects.all().first()
        campus = Campus.objects.all().first()

        with self.assertRaises(ValidationError):
            InstitutionCampus.objects.create(institution=institution, campus=campus)
            InstitutionCampus(institution=institution, campus=campus).validate_unique()


class AcademicEducationCampusTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)
        location = Location.objects.create(city=city, state=state)

        course = Course.objects.create(name=COURSE_NAME)
        grade = Grade.objects.create(name=GRADE_NAME)
        AcademicEducation.objects.create(course=course, grade=grade)

        Campus.objects.create(name=CAMPUS_NAME, location=location)

    def test_create_valid(self):
        campus = Campus.objects.all().first()
        academic_education = AcademicEducation.objects.all().first()

        academic_education_campus = AcademicEducationCampus.objects.create(
            academic_education=academic_education, campus=campus
        )

        self.assertNotEqual(academic_education_campus.id, None)
        self.assertEqual(academic_education_campus.campus, campus)
        self.assertEqual(academic_education_campus.academic_education, academic_education)
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 1)
        self.assertEqual(academic_education_campus.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            AcademicEducationCampus(academic_education=None).clean_fields()

        with self.assertRaises(ValidationError):
            AcademicEducationCampus(campus=None).clean_fields()

    def test_create_invalid_course_and_grade_instance(self):
        with self.assertRaises(ValueError):
            AcademicEducationCampus(academic_education="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducationCampus(campus="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducationCampus(academic_education=1).clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducationCampus(campus=1).clean_fields()

    def test_create_invalid_course_and_grade_unique_together(self):
        academic_education = AcademicEducation.objects.all().first()
        campus = Campus.objects.all().first()

        with self.assertRaises(ValidationError):
            AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
            AcademicEducationCampus(academic_education=academic_education, campus=campus).validate_unique()
