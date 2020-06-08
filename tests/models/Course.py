from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import AcademicEducation, Course, Grade
from nupe.core.models.Course import COURSE_MAX_LENGTH, GRADE_MAX_LENGTH
from resources.const.datas.Course import COURSE_NAME, GRADE_NAME


class CourseTestCase(TestCase):
    def test_create_valid(self):
        course = Course.objects.create(name=COURSE_NAME)

        self.assertNotEqual(course.id, None)  # o objeto criado deve conter um id
        self.assertEqual(course.name, COURSE_NAME)  # o objeto criado deve conter o nome fornecido
        self.assertEqual(Course.objects.all().count(), 1)  # o objeto deve ser criado no banco de dados
        self.assertEqual(course.full_clean(), None)  # o objeto não deve conter erros de validação

    def test_create_invalid_max_length(self):
        # passar do limite de caracteres deve emitir erro de validação
        with self.assertRaises(ValidationError):
            Course(name=COURSE_NAME * COURSE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        # deve emitir erro de que o campo não pode ser nulo
        with self.assertRaises(ValidationError):
            Course(name=None).clean_fields()

    def test_create_invalid_blank(self):
        # deve emitir erro de que o campo é obrigatório
        with self.assertRaises(ValidationError):
            Course().clean_fields()

        # deve emitir erro de que o campo não pode ser em branco
        with self.assertRaises(ValidationError):
            Course(name="").clean_fields()

        # deve emitir erro de que o campo não pode ser em branco porque espaços são ignorados
        with self.assertRaises(ValidationError):
            Course(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        # deve emitir erro porque só pode conter um único objeto com o mesmo nome
        with self.assertRaises(ValidationError):
            Course.objects.create(name=COURSE_NAME)
            Course(name=COURSE_NAME).validate_unique()

    def test_soft_delete_cascade(self):
        course = Course.objects.create(name=COURSE_NAME)
        grade = Grade.objects.create(name=GRADE_NAME)

        # a relação entre os objetos deve ser criada
        grade.courses.add(course)
        self.assertEqual(grade.courses.all().count(), 1)

        course.delete()
        # o objeto deve ser mascarado
        self.assertEqual(Course.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Course.all_objects.all().count(), 1)

        # o soft delete cascade deve ser aplicado
        self.assertEqual(grade.courses.all().count(), 0)

    def test_undelete(self):
        course = Course.objects.create(name=COURSE_NAME)
        grade = Grade.objects.create(name=GRADE_NAME)

        grade.courses.add(course)

        course.delete()

        course.undelete()
        # o objeto deve ser desmascarado
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(grade.courses.all().count(), 1)


class GradeTestCase(TestCase):
    def test_create_valid(self):
        grade = Grade.objects.create(name=GRADE_NAME)

        self.assertNotEqual(grade.id, None)
        self.assertEqual(grade.name, GRADE_NAME)
        self.assertEqual(Grade.objects.all().count(), 1)
        self.assertEqual(grade.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Grade(name=GRADE_NAME * GRADE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Grade(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Grade().clean_fields()

        with self.assertRaises(ValidationError):
            Grade(name="").clean_fields()

        with self.assertRaises(ValidationError):
            Grade(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name=GRADE_NAME)
            Grade(name=GRADE_NAME).validate_unique()

    def test_soft_delete_cascade(self):
        grade = Grade.objects.create(name=GRADE_NAME)
        course = Course.objects.create(name=COURSE_NAME)

        course.grades.add(grade)
        self.assertEqual(course.grades.all().count(), 1)

        grade.delete()
        self.assertEqual(Grade.objects.all().count(), 0)
        self.assertEqual(Grade.all_objects.all().count(), 1)
        self.assertEqual(course.grades.all().count(), 0)

    def test_undelete(self):
        grade = Grade.objects.create(name=GRADE_NAME)
        course = Course.objects.create(name=COURSE_NAME)

        course.grades.add(grade)

        grade.delete()

        grade.undelete()
        self.assertEqual(Grade.objects.all().count(), 1)
        self.assertEqual(course.grades.all().count(), 1)


class AcademicEducationTestCase(TestCase):
    def setUp(self):
        # cria no banco de dados de test antes de executar os tests
        Course.objects.create(name=COURSE_NAME)
        Grade.objects.create(name=GRADE_NAME)

    def test_create_valid(self):
        course = Course.objects.get(name=COURSE_NAME)
        grade = Grade.objects.get(name=GRADE_NAME)

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        self.assertNotEqual(academic_education.id, None)
        self.assertEqual(academic_education.course, course)
        self.assertEqual(academic_education.grade, grade)
        self.assertEqual(AcademicEducation.objects.all().count(), 1)
        self.assertEqual(academic_education.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            AcademicEducation(course=None).clean_fields()

        with self.assertRaises(ValidationError):
            AcademicEducation(grade=None).clean_fields()

    def test_create_invalid_course_and_grade_instance(self):
        # deve emitir um erro porque deve ser fornecido uma instancia de objeto do respectivo field

        with self.assertRaises(ValueError):
            AcademicEducation(course="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(grade="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(course=1).clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(grade=1).clean_fields()

    def test_create_invalid_course_and_grade_unique_together(self):
        course = Course.objects.get(name=COURSE_NAME)
        grade = Grade.objects.get(name=GRADE_NAME)

        # deve emitir um erro porque só pode exitir um objeto com o mesmo curso e grau
        with self.assertRaises(ValidationError):
            AcademicEducation.objects.create(course=course, grade=grade)
            AcademicEducation(course=course, grade=grade).validate_unique()

    def test_soft_delete_cascade(self):
        grade = Grade.objects.get(name=GRADE_NAME)
        course = Course.objects.get(name=COURSE_NAME)

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        academic_education.delete()
        self.assertEqual(AcademicEducation.objects.all().count(), 0)
        self.assertEqual(AcademicEducation.all_objects.all().count(), 1)

    def test_undelete(self):
        grade = Grade.objects.get(name=GRADE_NAME)
        course = Course.objects.get(name=COURSE_NAME)

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        academic_education.delete()
        self.assertEqual(AcademicEducation.objects.all().count(), 0)

        academic_education.undelete()
        self.assertEqual(AcademicEducation.objects.all().count(), 1)

        grade.delete()
        self.assertEqual(AcademicEducation.objects.all().count(), 0)

        grade.undelete()
        self.assertEqual(AcademicEducation.objects.all().count(), 1)

        course.delete()
        self.assertEqual(AcademicEducation.objects.all().count(), 0)

        course.undelete()
        self.assertEqual(AcademicEducation.objects.all().count(), 1)
