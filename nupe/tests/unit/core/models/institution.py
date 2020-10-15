from django.test import TestCase
from model_bakery import baker

from nupe.core.models import Campus, Institution


class InstitutionTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Institution, "_safedelete_policy"), True)
        self.assertIs(hasattr(Institution, "name"), True)
        self.assertIs(hasattr(Institution, "campus"), True)

    def test_return_str(self):
        institution = baker.prepare(Institution)

        self.assertEqual(str(institution), institution.name)


class CampusTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Campus, "_safedelete_policy"), True)
        self.assertIs(hasattr(Campus, "name"), True)
        self.assertIs(hasattr(Campus, "cnpj"), True)
        self.assertIs(hasattr(Campus, "address"), True)
        self.assertIs(hasattr(Campus, "number"), True)
        self.assertIs(hasattr(Campus, "website"), True)
        self.assertIs(hasattr(Campus, "location"), True)
        self.assertIs(hasattr(Campus, "institution"), True)
        self.assertIs(hasattr(Campus, "academic_education_campus"), True)
        self.assertIs(hasattr(Campus, "workers"), True)

    def test_return_str(self):
        campus = baker.prepare(Campus)

        str_expected = f"{campus.institution} - {campus.name}"
        self.assertEqual(str(campus), str_expected)
