from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import (
    CAMPUS_MAX_LENGTH,
    INSTITUTION_MAX_LENGTH,
    AcademicEducation,
    AcademicEducationCampus,
    Campus,
    Institution,
    InstitutionCampus,
    Location,
)
from tests.models.Course import COURSE_NAME, GRADE_NAME
from tests.models.Location import CITY_NAME, STATE_NAME
from tests.models.setup import setup_create_academic_education, setup_create_location

INSTITUTION_NAME = "Instituto Federal Catarinense"
CAMPUS_NAME = "Araquari"


class InstitutionTestCase(TestCase):
    def test_create_valid(self):
        institution = Institution.objects.create(name=INSTITUTION_NAME)

        self.assertNotEqual(institution.id, None)  # o objeto criado deve conter um id
        self.assertEqual(institution.name, INSTITUTION_NAME)  # o objeto criado deve conter o nome fornecido
        self.assertEqual(Institution.objects.all().count(), 1)  # o objeto deve ser criado no banco de dados
        self.assertEqual(institution.full_clean(), None)  # o objeto não deve conter erros de validação

    def test_create_invalid_max_length(self):
        # passar do limite de caracteres deve emitir erro de validação
        with self.assertRaises(ValidationError):
            Institution(name=INSTITUTION_NAME * INSTITUTION_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        # deve emitir erro de que o campo não pode ser nulo
        with self.assertRaises(ValidationError):
            Institution(name=None).clean_fields()

    def test_create_invalid_blank(self):
        # deve emitir erro de que o campo é obrigatório
        with self.assertRaises(ValidationError):
            Institution().clean_fields()

        # deve emitir erro de que o campo não pode ser em branco
        with self.assertRaises(ValidationError):
            Institution(name="").clean_fields()

        # deve emitir erro de que o campo não pode ser em branco porque espaços são ignorados
        with self.assertRaises(ValidationError):
            Institution(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        # deve emitir erro porque só pode conter um único objeto com o mesmo nome
        with self.assertRaises(ValidationError):
            Institution.objects.create(name=INSTITUTION_NAME)
            Institution(name=INSTITUTION_NAME).validate_unique()

    def test_no_delete(self):
        location = setup_create_location(city_name=CITY_NAME, state_name=STATE_NAME)

        institution = Institution.objects.create(name=INSTITUTION_NAME)
        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)

        # a relação entre os objetos deve ser criada
        campus.institutions.add(institution)

        institution.delete()
        # o objeto não deve ser mascarado e nem excluído do banco de dados
        self.assertEqual(Institution.objects.all().count(), 1)

        # a relação deve permanecer
        self.assertEqual(campus.institutions.all().count(), 1)


class CampusTestCase(TestCase):
    def setUp(self):
        # cria no banco de dados de test antes de executar os tests
        setup_create_location(city_name=CITY_NAME, state_name=STATE_NAME)

    def test_create_valid(self):
        location = Location.objects.get(city__name=CITY_NAME, state__name=STATE_NAME)

        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)

        self.assertNotEqual(campus.id, None)
        self.assertEqual(campus.name, CAMPUS_NAME)
        self.assertEqual(campus.location, location)
        self.assertEqual(Campus.objects.all().count(), 1)
        self.assertEqual(campus.full_clean(), None)

    def test_create_invalid_max_length(self):
        location = Location.objects.get(city__name=CITY_NAME, state__name=STATE_NAME)

        with self.assertRaises(ValidationError):
            Campus(name=CAMPUS_NAME * CAMPUS_MAX_LENGTH, location=location).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Campus(name=None).clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=None).clean_fields()

    def test_create_invalid_blank(self):
        location = Location.objects.get(city__name=CITY_NAME, state__name=STATE_NAME)

        with self.assertRaises(ValidationError):
            Campus().clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=location, name="").clean_fields()

        with self.assertRaises(ValidationError):
            Campus(location=location, name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        location = Location.objects.get(city__name=CITY_NAME, state__name=STATE_NAME)

        with self.assertRaises(ValidationError):
            Campus.objects.create(name=CAMPUS_NAME, location=location)
            Campus(name=CAMPUS_NAME, location=location).validate_unique()

    def test_no_delete(self):
        location = Location.objects.get(city__name=CITY_NAME, state__name=STATE_NAME)

        campus = Campus.objects.create(name=CAMPUS_NAME, location=location)
        institution = Institution.objects.create(name=INSTITUTION_NAME)

        institution.campus.add(campus)

        campus.delete()
        self.assertEqual(Campus.objects.all().count(), 1)
        self.assertEqual(institution.campus.all().count(), 1)


class InstitutionCampusTestCase(TestCase):
    def setUp(self):
        location = setup_create_location(city_name=CITY_NAME, state_name=STATE_NAME)

        Institution.objects.create(name=INSTITUTION_NAME)
        Campus.objects.create(name=CAMPUS_NAME, location=location)

    def test_create_valid(self):
        institution = Institution.objects.get(name=INSTITUTION_NAME)
        campus = Campus.objects.get(name=CAMPUS_NAME)

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
        # deve emitir um erro porque deve ser fornecido uma instancia de objeto do respectivo field

        with self.assertRaises(ValueError):
            InstitutionCampus(institution="").clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(campus="").clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(institution=1).clean_fields()

        with self.assertRaises(ValueError):
            InstitutionCampus(campus=1).clean_fields()

    def test_create_invalid_course_and_grade_unique_together(self):
        institution = Institution.objects.get(name=INSTITUTION_NAME)
        campus = Campus.objects.get(name=CAMPUS_NAME)

        # deve emitir um erro porque só pode exitir um objeto com o mesmo instituto e campus
        with self.assertRaises(ValidationError):
            InstitutionCampus.objects.create(institution=institution, campus=campus)
            InstitutionCampus(institution=institution, campus=campus).validate_unique()

    def test_no_delete(self):
        campus = Campus.objects.get(name=CAMPUS_NAME)
        institution = Institution.objects.get(name=INSTITUTION_NAME)

        institution_campus = InstitutionCampus.objects.create(institution=institution, campus=campus)

        institution_campus.delete()
        self.assertEqual(InstitutionCampus.objects.all().count(), 1)


class AcademicEducationCampusTestCase(TestCase):
    def setUp(self):
        setup_create_academic_education(course_name=COURSE_NAME, grade_name=GRADE_NAME)
        location = setup_create_location(city_name=CITY_NAME, state_name=STATE_NAME)

        Campus.objects.create(name=CAMPUS_NAME, location=location)

    def test_create_valid(self):
        campus = Campus.objects.get(name=CAMPUS_NAME)
        academic_education = AcademicEducation.objects.get(course__name=COURSE_NAME, grade__name=GRADE_NAME)

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
        academic_education = AcademicEducation.objects.get(course__name=COURSE_NAME, grade__name=GRADE_NAME)
        campus = Campus.objects.get(name=CAMPUS_NAME)

        with self.assertRaises(ValidationError):
            AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
            AcademicEducationCampus(academic_education=academic_education, campus=campus).validate_unique()

    def test_no_delete(self):
        campus = Campus.objects.get(name=CAMPUS_NAME)
        academic_education = AcademicEducation.objects.get(course__name=COURSE_NAME, grade__name=GRADE_NAME)

        academic_education_campus = AcademicEducationCampus.objects.create(
            academic_education=academic_education, campus=campus
        )
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 1)

        campus.delete()
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 1)

        academic_education.delete()
        # a model AcademicEducation tem a policy definida como soft_delete_cascade, por isso, deve ser mascarado
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(AcademicEducationCampus.all_objects.all().count(), 1)

        academic_education.undelete()  # restaura o dado para testar novamente

        academic_education_campus.delete()
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(AcademicEducationCampus.all_objects.all().count(), 1)

    def test_undelete(self):
        campus = Campus.objects.get(name=CAMPUS_NAME)
        academic_education = AcademicEducation.objects.get(course__name=COURSE_NAME, grade__name=GRADE_NAME)

        academic_education_campus = AcademicEducationCampus.objects.create(
            academic_education=academic_education, campus=campus
        )

        academic_education.delete()
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 0)

        academic_education.undelete()
        # o objeto deve ser desmascarado
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 1)

        academic_education_campus.delete()
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 0)

        academic_education_campus.undelete()
        self.assertEqual(AcademicEducationCampus.objects.all().count(), 1)
