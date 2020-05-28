from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import STUDENT_REGISTRATION_MAX_LENGTH, AcademicEducationCampus, Person, Responsible, Student
from tests.models.Course import COURSE_NAME, GRADE_NAME
from tests.models.Institution import CAMPUS_NAME
from tests.models.Location import CITY_NAME, STATE_NAME
from tests.models.Person import (
    BIRTHDAY_DATE,
    CPF,
    CPF_2,
    CPF_3,
    FIRST_NAME,
    GENDER,
    LAST_NAME,
    RG,
    RG_2,
    RG_3,
    UNDER_AGE_BIRTHDAY_DATE,
)
from tests.models.setup import setup_create_academic_education_campus

REGISTRATION = "202026050001"
INGRESS_DATE = "2020-05-26"


class StudentTestCase(TestCase):
    def setUp(self):
        setup_create_academic_education_campus(
            course_name=COURSE_NAME,
            grade_name=GRADE_NAME,
            city_name=CITY_NAME,
            state_name=STATE_NAME,
            campus_name=CAMPUS_NAME,
        )

        Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )
        Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF_2, rg=RG_2, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )

    def test_create_valid(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person = Person.objects.get(cpf=CPF)

        student = Student.objects.create(
            registration=REGISTRATION,
            person=person,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )

        self.assertNotEqual(student.id, None)  # o objeto criado deve conter um id
        self.assertEqual(student.person.id, person.id)  # o objeto criado deve conter a pessoa fornecida
        self.assertEqual(Student.objects.all().count(), 1)  # o objeto deve ser criado no banco de dados
        self.assertEqual(student.full_clean(), None)  # o objeto não deve conter erros de validação

    def test_create_invalid_max_length(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person = Person.objects.get(cpf=CPF)

        with self.assertRaises(ValidationError):
            Student(
                registration="1" * (STUDENT_REGISTRATION_MAX_LENGTH + 1),
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

    def test_create_invalid_null(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person = Person.objects.get(cpf=CPF)

        with self.assertRaises(ValidationError):
            Student(
                registration=None,
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION,
                person=None,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION, person=person, academic_education_campus=None, ingress_date=INGRESS_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION,
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=None,
            ).clean_fields()

    def test_create_invalid_blank(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person = Person.objects.get(cpf=CPF)

        # deve emitir erro de que os campos são obrigatórios
        with self.assertRaises(ValidationError):
            Student().clean_fields()

        # deve emitir erro de que o campo não pode ser em branco
        with self.assertRaises(ValidationError):
            Student(
                registration="",
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=" ",
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION,
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date="",
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION,
                person=person,
                academic_education_campus=academic_education_campus,
                ingress_date=" ",
            ).clean_fields()

    def test_create_invalid_unique_and_unique_together(self):
        """
        testa unique para registration e
        unique together para person e academic_education_campus
        """
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person1 = Person.objects.get(cpf=CPF)
        person2 = Person.objects.get(cpf=CPF_2)

        Student.objects.create(
            registration=REGISTRATION,
            person=person1,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )

        # deve emitir erro porque só pode conter um único objeto com a mesma matrícula
        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION,
                person=person2,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).validate_unique()

        # deve emitir erro porque o estudante não pode realizar uma nova matrícula no mesmo curso
        with self.assertRaises(ValidationError):
            Student(
                registration=REGISTRATION + "1",
                person=person1,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).validate_unique()

    def test_invalid_regex(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person1 = Person.objects.get(cpf=CPF)

        # registration deve conter somente números
        with self.assertRaises(ValidationError):
            Student(
                registration="kfdmsfmdsk",
                person=person1,
                academic_education_campus=academic_education_campus,
                ingress_date=INGRESS_DATE,
            ).clean_fields()

    def test_properties(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person1 = Person.objects.get(cpf=CPF)

        student = Student.objects.create(
            registration=REGISTRATION,
            person=person1,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )

        self.assertEqual(student.age, person1.age)
        self.assertEqual(student.academic_education, str(academic_education_campus.academic_education))

    def test_soft_delete_cascade(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person1 = Person.objects.get(cpf=CPF)
        person2 = Person.objects.get(cpf=CPF_2)

        student = Student.objects.create(
            registration=REGISTRATION,
            person=person1,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )
        student.responsibles_persons.add(person2)

        person2.delete()  # remove o responsável

        # o responsável deve ser mascarado
        self.assertEqual(student.responsibles_persons.all().count(), 0)
        self.assertEqual(Responsible.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Responsible.all_objects.all().count(), 1)

        # on delete SET_NULL deve ser aplicado
        academic_education_campus.delete()
        self.assertEqual(Student.objects.all().count(), 1)

        # reload da instância do estudante após o campo ser setado como None
        student = Student.objects.get(registration=REGISTRATION)
        self.assertEqual(student.academic_education_campus, None)

        # quando as informações do estudante são removidas, o estudante também deve ser
        person1.delete()
        self.assertEqual(Student.objects.all().count(), 0)

    def test_undelete(self):
        academic_education_campus = AcademicEducationCampus.objects.all().first()
        person1 = Person.objects.get(cpf=CPF)
        person2 = Person.objects.get(cpf=CPF_2)

        student = Student.objects.create(
            registration=REGISTRATION,
            person=person1,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )
        student.responsibles_persons.add(person2)

        person2.delete()

        person2.undelete()

        # o responsável deve ser restaurado
        self.assertEqual(student.responsibles_persons.all().count(), 1)
        self.assertEqual(Responsible.objects.all().count(), 1)

        academic_education_campus.delete()

        academic_education_campus.undelete()
        student_reload = Student.objects.get(registration=REGISTRATION)

        # academic_education_campus deve ser restaurado para o valor anterior
        self.assertEqual(student_reload.academic_education_campus, student.academic_education_campus)

        person1.delete()

        person1.undelete()

        # quando as informações do estudante são restauradas, o estudante também deve ser
        self.assertEqual(Student.objects.all().count(), 1)


class ResponsibleTestCase(TestCase):
    def setUp(self):
        academic_education_campus = setup_create_academic_education_campus(
            course_name=COURSE_NAME,
            grade_name=GRADE_NAME,
            city_name=CITY_NAME,
            state_name=STATE_NAME,
            campus_name=CAMPUS_NAME,
        )

        person1 = Person.objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            cpf=CPF,
            rg=RG,
            birthday_date=UNDER_AGE_BIRTHDAY_DATE,
            gender=GENDER,
        )

        Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF_2, rg=RG_2, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )

        Person.objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            cpf=CPF_3,
            rg=RG_3,
            birthday_date=UNDER_AGE_BIRTHDAY_DATE,
            gender=GENDER,
        )

        Student.objects.create(
            registration=REGISTRATION,
            person=person1,
            academic_education_campus=academic_education_campus,
            ingress_date=INGRESS_DATE,
        )

    def test_create_valid(self):
        student = Student.objects.get(registration=REGISTRATION)
        person = Person.objects.get(cpf=CPF_2)

        responsible = Responsible.objects.create(student=student, person=person)

        self.assertNotEqual(responsible.id, None)
        self.assertEqual(responsible.person, person)
        self.assertEqual(Responsible.objects.all().count(), 1)
        self.assertEqual(responsible.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Responsible(student=None).clean_fields()

        with self.assertRaises(ValidationError):
            Responsible(person=None).clean_fields()

    def test_create_invalid_student_and_person_instance(self):
        # deve emitir um erro porque deve ser fornecido uma instancia de objeto do respectivo field

        with self.assertRaises(ValueError):
            Responsible.objects.create(student="")

        with self.assertRaises(ValueError):
            Responsible.objects.create(person="")

        with self.assertRaises(ValueError):
            Responsible.objects.create(student=1)

        with self.assertRaises(ValueError):
            Responsible.objects.create(person=1)

    def test_create_invalid_student_and_person_unique_together(self):
        student = Student.objects.get(registration=REGISTRATION)
        person = Person.objects.get(cpf=CPF_2)

        # deve emitir um erro porque só pode exitir um objeto para a mesma pessoa e estudante
        with self.assertRaises(ValidationError):
            Responsible.objects.create(student=student, person=person)
            Responsible(student=student, person=person).validate_unique()

    def test_create_invalid_responsible(self):
        student = Student.objects.get(registration=REGISTRATION)
        student_person = Person.objects.get(cpf=CPF)
        under_age_person = Person.objects.get(cpf=CPF_3)

        # deve emitir um erro porque o responsável não pode ser o próprio estudante se o estudante for menor de idade
        with self.assertRaises(ValidationError):
            Responsible(student=student, person=student_person).clean()

        # deve emitir um erro porque o responsável não pode ser menor de idade
        with self.assertRaises(ValidationError):
            Responsible(student=student, person=under_age_person).clean()

    def test_soft_delete(self):
        student = Student.objects.get(registration=REGISTRATION)
        person = Person.objects.get(cpf=CPF_2)

        responsible = Responsible.objects.create(student=student, person=person)

        self.assertEqual(Responsible.objects.all().count(), 1)

        responsible.delete()

        self.assertEqual(Responsible.objects.all().count(), 0)
        self.assertEqual(Responsible.all_objects.all().count(), 1)

    def test_undelete(self):
        student = Student.objects.get(registration=REGISTRATION)
        person = Person.objects.get(cpf=CPF_2)

        responsible = Responsible.objects.create(student=student, person=person)

        responsible.delete()

        responsible.undelete()
        self.assertEqual(Responsible.objects.all().count(), 1)
