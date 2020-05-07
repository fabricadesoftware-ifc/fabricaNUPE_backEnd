from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import (
    PERSON_CONTACT_MAX_LENGTH,
    PERSON_CONTACT_MIN_LENGTH,
    PERSON_CPF_MAX_LENGTH,
    PERSON_CPF_MIN_LENGTH,
    PERSON_FIRST_NAME_MAX_LENGTH,
    PERSON_GENDER_MAX_LENGTH,
    PERSON_LAST_NAME_MAX_LENGTH,
    PERSON_RG_MAX_LENGTH,
    PERSON_RG_MIN_LENGTH,
    Person,
)

# dados válidos

FIRST_NAME = "a"
LAST_NAME = "b"
CPF = "59886572060"
RG = "1234567"
DATE = {"date": "11/11/2011", "format": "%d/%m/%Y"}
BORN_DATE = datetime.strptime(DATE["date"], DATE["format"]).date()
GENDER = "M"
CONTACT = "047999999999"
AGE = datetime.now().year - BORN_DATE.year
FULL_NAME = "{} {}".format(FIRST_NAME, LAST_NAME)

CPF_2 = "45820105044"
RG_2 = "1234567"


# dados inválidos

INVALID_NAME = "jose43"
INVALID_CPF = "11864707985"
INVALID_RG = "abcdef@"
INVALID_CONTACT = "9 9168-2452"

INVALID_NAME_2 = "jose@!"
INVALID_CPF_2 = "118647079@l"
INVALID_RG_2 = "123456l"
INVALID_CONTACT_2 = "47-991682452"

INVALID_CPF_LENGTH = "1" * (PERSON_CPF_MIN_LENGTH - 1)
INVALID_RG_LENGTH = "2" * (PERSON_RG_MIN_LENGTH - 1)
INVALID_CONTACT_LENGTH = "9" * (PERSON_CONTACT_MIN_LENGTH - 1)


class PersonTestCase(TestCase):
    def test_create_valid(self):
        person = Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, born_date=BORN_DATE, gender=GENDER,
        )

        self.assertNotEqual(person.id, None)
        self.assertEqual(person.cpf, CPF)
        self.assertEqual(Person.objects.all().count(), 1)
        self.assertEqual(person.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME * (PERSON_FIRST_NAME_MAX_LENGTH + 1),
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME * (PERSON_LAST_NAME_MAX_LENGTH + 1),
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF * (PERSON_CPF_MAX_LENGTH + 1),
                rg=RG,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG * (PERSON_RG_MAX_LENGTH + 1),
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER * (PERSON_GENDER_MAX_LENGTH + 1),
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                contact=CONTACT * (PERSON_CONTACT_MAX_LENGTH + 1),
                born_date=BORN_DATE,
            ).clean_fields()

    def test_create_invalid_min_length(self):
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=INVALID_CPF_LENGTH,
                rg=RG,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=INVALID_RG_LENGTH,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                contact=INVALID_CONTACT_LENGTH,
                born_date=BORN_DATE,
            ).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Person(
                first_name=None, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=None, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=None, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=None, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=None, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=None,
            ).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Person().clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name="", last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=" ", last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name="", cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=" ", cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf="", rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=" ", rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).full_clean()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg="", gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=" ", gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender="", born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=" ", born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date="",
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=" ",
            ).clean_fields()

    def test_create_invalid_unique_cpf_and_rg(self):
        Person.objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            cpf=CPF,
            rg=RG,
            gender=GENDER,
            contact=CONTACT,
            born_date=BORN_DATE,
        )

        # teste CPF
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG_2,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).validate_unique()

        # teste RG
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF_2,
                rg=RG,
                gender=GENDER,
                contact=CONTACT,
                born_date=BORN_DATE,
            ).validate_unique()

    def test_create_invalid_regex(self):
        # first_name deve conter somente letras e espaço
        with self.assertRaises(ValidationError):
            Person(
                first_name=INVALID_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=INVALID_NAME_2, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        # last_name deve conter somente letras e espaço
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=INVALID_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=INVALID_NAME_2, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        # cpf deve ser um documento valido
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=INVALID_CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
            ).clean()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=INVALID_CPF_2,
                rg=RG,
                gender=GENDER,
                born_date=BORN_DATE,
            ).clean()

        # rg deve conter somente numeros
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=INVALID_RG, gender=GENDER, born_date=BORN_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=INVALID_RG_2,
                gender=GENDER,
                born_date=BORN_DATE,
            ).clean_fields()

        # contact deve conter somente numeros
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                born_date=BORN_DATE,
                contact=INVALID_CONTACT,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                rg=RG,
                gender=GENDER,
                born_date=BORN_DATE,
                contact=INVALID_CONTACT_2,
            ).clean_fields()

    def test_properties(self):
        person = Person(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, born_date=BORN_DATE,
        )

        self.assertNotEqual(person.age, None)
        self.assertNotEqual(person.full_name, None)
        self.assertEqual(person.age, AGE)
        self.assertEqual(person.full_name, FULL_NAME)
