from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import Person
from nupe.core.models.person import (
    PERSON_CONTACT_MAX_LENGTH,
    PERSON_CPF_MAX_LENGTH,
    PERSON_FIRST_NAME_MAX_LENGTH,
    PERSON_GENDER_MAX_LENGTH,
    PERSON_LAST_NAME_MAX_LENGTH,
)
from resources.const.datas.person import (
    AGE,
    BIRTHDAY_DATE,
    CONTACT,
    CPF,
    FIRST_NAME,
    FULL_NAME,
    GENDER,
    INVALID_CONTACT,
    INVALID_CONTACT_2,
    INVALID_CONTACT_LENGTH,
    INVALID_CPF_LENGTH,
    INVALID_NAME,
    INVALID_NAME_2,
    LAST_NAME,
)


class PersonTestCase(TestCase):
    def test_create_valid(self):
        person = Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )

        self.assertNotEqual(person.id, None)  # o objeto criado deve conter um id
        self.assertEqual(person.cpf, CPF)  # o objeto criado deve conter o cpf fornecido
        self.assertEqual(Person.objects.all().count(), 1)  # o objeto deve ser criado no banco de dados
        self.assertEqual(person.full_clean(), None)  # o objeto não deve conter erros de validação

    def test_create_invalid_max_length(self):
        # passar do limite de caracteres deve emitir erro de validação

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME * (PERSON_FIRST_NAME_MAX_LENGTH + 1),
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME * (PERSON_LAST_NAME_MAX_LENGTH + 1),
                cpf=CPF,
                gender=GENDER,
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF * (PERSON_CPF_MAX_LENGTH + 1),
                gender=GENDER,
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER * (PERSON_GENDER_MAX_LENGTH + 1),
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                contact=CONTACT * (PERSON_CONTACT_MAX_LENGTH + 1),
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

    def test_create_invalid_min_length(self):
        # não conter o mínimo de caracteres deve emitir erro de validação

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=INVALID_CPF_LENGTH,
                gender=GENDER,
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

    def test_create_invalid_null(self):
        # deve emitir erro de que o campo não pode ser nulo

        with self.assertRaises(ValidationError):
            Person(
                first_name=None, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=None, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=None, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, gender=None, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=None,
            ).clean_fields()

    def test_create_invalid_blank(self):
        # deve emitir erro de que os campos são obrigatórios
        with self.assertRaises(ValidationError):
            Person().clean_fields()

        # deve emitir erro de que o campo não pode ser em branco
        with self.assertRaises(ValidationError):
            Person(
                first_name="", last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name="", cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf="", gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, gender="", birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date="",
            ).clean_fields()

    def test_create_invalid_unique_cpf(self):
        Person.objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            cpf=CPF,
            gender=GENDER,
            contact=CONTACT,
            birthday_date=BIRTHDAY_DATE,
        )

        # deve emitir erro porque só pode conter um único objeto com o mesmo cpf
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                contact=CONTACT,
                birthday_date=BIRTHDAY_DATE,
            ).validate_unique()

    def test_create_invalid_regex(self):
        # first_name deve conter somente letras e espaço
        with self.assertRaises(ValidationError):
            Person(
                first_name=INVALID_NAME, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=INVALID_NAME_2, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        # last_name deve conter somente letras e espaço
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=INVALID_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME, last_name=INVALID_NAME_2, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
            ).clean_fields()

        # contact deve conter somente numeros
        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                birthday_date=BIRTHDAY_DATE,
                contact=INVALID_CONTACT,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                birthday_date=BIRTHDAY_DATE,
                contact=INVALID_CONTACT_2,
            ).clean_fields()

        with self.assertRaises(ValidationError):
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                cpf=CPF,
                gender=GENDER,
                birthday_date=BIRTHDAY_DATE,
                contact=INVALID_CONTACT_LENGTH,
            ).clean_fields()

    def test_properties(self):
        person = Person(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, gender=GENDER, birthday_date=BIRTHDAY_DATE,
        )

        self.assertNotEqual(person.age, None)  # deve retornar um inteiro com a idade da pessoa
        self.assertNotEqual(person.full_name, None)  # deve retornar uma string com o nome e o sobrenome juntos
        self.assertEqual(person.age, AGE)  # a idade deve estar correta
        self.assertEqual(person.full_name, FULL_NAME)  # o nome completo deve ser a junção do nome com o sobrenome

    def test_soft_delete(self):
        person = Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )

        person.delete()
        # o objeto deve ser mascarado
        self.assertEqual(Person.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.all().count(), 1)

    def test_undelete(self):
        person = Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, birthday_date=BIRTHDAY_DATE, gender=GENDER,
        )

        person.delete()

        person.undelete()
        # o objeto deve ser desmascarado
        self.assertEqual(Person.objects.all().count(), 1)
