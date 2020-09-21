from django.test import TestCase
from model_bakery import baker

from nupe.core.models import Person
from nupe.core.utils.properties import calculate_age


class PersonTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Person, "_safedelete_policy"), True)
        self.assertIs(hasattr(Person, "first_name"), True)
        self.assertIs(hasattr(Person, "last_name"), True)
        self.assertIs(hasattr(Person, "cpf"), True)
        self.assertIs(hasattr(Person, "birthday_date"), True)
        self.assertIs(hasattr(Person, "gender"), True)
        self.assertIs(hasattr(Person, "contact"), True)
        self.assertIs(hasattr(Person, "profile_image"), True)
        self.assertIs(hasattr(Person, "created_at"), True)
        self.assertIs(hasattr(Person, "updated_at"), True)
        self.assertIs(hasattr(Person, "student_registrations"), True)
        self.assertIs(hasattr(Person, "dependents"), True)
        self.assertIs(hasattr(Person, "responsibles"), True)

    def test_return_str(self):
        person = baker.prepare(Person)

        self.assertEqual(str(person), person.full_name)

    def test_return_properties(self):
        person = baker.prepare(Person)

        full_name_expected = f"{person.first_name} {person.last_name}"
        self.assertEqual(person.full_name, full_name_expected)

        age_expected = calculate_age(birthday_date=person.birthday_date)
        self.assertEqual(person.age, age_expected)
