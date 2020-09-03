from django.test import TestCase
from model_bakery import baker

from nupe.core.models import City, Location, State


class CityTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(City, "_safedelete_policy"), True)
        self.assertIs(hasattr(City, "name"), True)

    def test_return_str(self):
        city = baker.prepare(City)

        self.assertEqual(str(city), city.name)


class StateTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(State, "_safedelete_policy"), True)
        self.assertIs(hasattr(State, "name"), True)
        self.assertIs(hasattr(State, "initials"), True)
        self.assertIs(hasattr(State, "cities"), True)

    def test_return_str(self):
        state = baker.prepare(State)

        self.assertEqual(str(state), state.name)


class LocationTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Location, "_safedelete_policy"), True)
        self.assertIs(hasattr(Location, "city"), True)
        self.assertIs(hasattr(Location, "state"), True)

    def test_return_str(self):
        location = baker.prepare(Location)

        str_expected = f"{location.city} - {location.state.initials}"
        self.assertEqual(str(location), str_expected)
