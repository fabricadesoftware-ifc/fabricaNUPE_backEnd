from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import CITY_MAX_LENGTH, STATE_MAX_LENGTH, City, Location, State

CITY_NAME = "Joinville"
STATE_NAME = "Santa Catarina"


class CityTestCase(TestCase):
    def test_create_valid(self):
        city = City.objects.create(name=CITY_NAME)

        self.assertNotEqual(city.id, None)
        self.assertEqual(city.name, CITY_NAME)
        self.assertEqual(City.objects.all().count(), 1)
        self.assertEqual(city.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            City(name=CITY_NAME * CITY_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            City(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            City().clean_fields()

        with self.assertRaises(ValidationError):
            City(name="").clean_fields()

        with self.assertRaises(ValidationError):
            City(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name=CITY_NAME)
            City(name=CITY_NAME).validate_unique()


class StateTestCase(TestCase):
    def test_create_valid(self):
        state = State.objects.create(name=STATE_NAME)

        self.assertNotEqual(state.id, None)
        self.assertEqual(state.name, STATE_NAME)
        self.assertEqual(State.objects.all().count(), 1)
        self.assertEqual(state.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            State(name=STATE_NAME * STATE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            State(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            State().clean_fields()

        with self.assertRaises(ValidationError):
            State(name="").clean_fields()

        with self.assertRaises(ValidationError):
            State(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name=STATE_NAME)
            State(name=STATE_NAME).validate_unique()


class LocationTestCase(TestCase):
    def setUp(self):
        City.objects.create(name=CITY_NAME)
        State.objects.create(name=STATE_NAME)

    def test_create_valid(self):
        city = City.objects.all().first()
        state = State.objects.all().first()

        location = Location.objects.create(city=city, state=state)

        self.assertNotEqual(location.id, None)
        self.assertEqual(location.city, city)
        self.assertEqual(location.state, state)
        self.assertEqual(Location.objects.all().count(), 1)
        self.assertEqual(location.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Location(city=None).clean_fields()

        with self.assertRaises(ValidationError):
            Location(state=None).clean_fields()

    def test_create_invalid_city_and_state_instance(self):
        with self.assertRaises(ValueError):
            Location.objects.create(city="")

        with self.assertRaises(ValueError):
            Location.objects.create(state="")

        with self.assertRaises(ValueError):
            Location.objects.create(city=1)

        with self.assertRaises(ValueError):
            Location.objects.create(state=1)

    def test_create_invalid_city_and_state_unique_together(self):
        city = City.objects.all().first()
        state = State.objects.all().first()

        with self.assertRaises(ValidationError):
            Location.objects.create(city=city, state=state)
            Location(city=city, state=state).validate_unique()
