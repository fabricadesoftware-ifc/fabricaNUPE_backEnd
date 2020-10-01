from django.test import TestCase
from model_bakery import baker

from nupe.core.models import Function, Sector


class FunctionTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Function, "_safedelete_policy"), True)
        self.assertIs(hasattr(Function, "name"), True)
        self.assertIs(hasattr(Function, "description"), True)
        self.assertIs(hasattr(Function, "workers"), True)

    def test_return_str(self):
        function = baker.prepare(Function)

        self.assertEqual(str(function), function.name)


class SectorTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Sector, "_safedelete_policy"), True)
        self.assertIs(hasattr(Sector, "name"), True)
        self.assertIs(hasattr(Sector, "description"), True)
        self.assertIs(hasattr(Sector, "workers"), True)

    def test_return_str(self):
        sector = baker.prepare(Sector)

        self.assertEqual(str(sector), sector.name)
