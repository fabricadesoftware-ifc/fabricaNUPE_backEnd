from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import City, Location, State, CITY_MAX_LENGTH, STATE_MAX_LENGTH

city_name = "Joinville"
state_name = "Santa Catarina"


class CityTestCase(TestCase):
    def test_create_valid(self):
        city = City.objects.create(name=city_name)
        self.assertEqual(city.name, city_name)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name=city_name * CITY_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            City.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name=city_name)
            City.objects.create(name=city_name)


class StateTestCase(TestCase):
    def test_create_valid(self):
        state = State.objects.create(name=state_name)
        self.assertEqual(state.name, state_name)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name=state_name * STATE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            State.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            State.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            State.objects.create(name=state_name)
            State.objects.create(name=state_name)


class LocationTestCase(TestCase):
    def test_create_valid(self):
        city = City.objects.create(name=city_name)
        state = State.objects.create(name=state_name)

        location = Location.objects.create(city=city, state=state)

        self.assertEqual(location.city.name, city_name)
        self.assertEqual(location.state.name, state_name)
        self.assertEqual(Location.objects.all().count(), 1)

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            Location.objects.create()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValueError):
            Location.objects.create(city="", state="")

    def test_create_invalid_city_and_state_instance(self):
        with self.assertRaises(ValueError):
            Location.objects.create(city=1, state=1)

    def test_create_invalid_city_and_state_unique_together(self):
        city = City.objects.create(name=city_name)
        state = State.objects.create(name=state_name)

        with self.assertRaises(IntegrityError):
            Location.objects.create(city=city, state=state)
            Location.objects.create(city=city, state=state)
