from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import CITY_MAX_LENGTH, STATE_MAX_LENGTH, City, Location, State

CITY_NAME = "Joinville"
STATE_NAME = "Santa Catarina"


class CityTestCase(TestCase):
    def test_create_valid(self):
        city = City.objects.create(name=CITY_NAME)
        self.assertEqual(city.name, CITY_NAME)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name=CITY_NAME * CITY_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            City.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name=CITY_NAME)
            City.objects.create(name=CITY_NAME)


class StateTestCase(TestCase):
    def test_create_valid(self):
        state = State.objects.create(name=STATE_NAME)
        self.assertEqual(state.name, STATE_NAME)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name=STATE_NAME * STATE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(IntegrityError):
            State.objects.create(name=None)

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            State.objects.create().clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(IntegrityError):
            State.objects.create(name=STATE_NAME)
            State.objects.create(name=STATE_NAME)


class LocationTestCase(TestCase):
    def setUp(self):
        City.objects.create(name=CITY_NAME)
        State.objects.create(name=STATE_NAME)

    def test_create_valid(self):
        city = City.objects.all().first()
        state = State.objects.all().first()

        location = Location.objects.create(city=city, state=state)

        self.assertEqual(location.city.name, CITY_NAME)
        self.assertEqual(location.state.name, STATE_NAME)
        self.assertEqual(Location.objects.all().count(), 1)

    def test_create_invalid_null(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Location.objects.create(city=None)

        with self.assertRaises(IntegrityError):
            Location.objects.create(state=None)

    def test_create_invalid_blank(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                Location.objects.create(city="")

        with self.assertRaises(ValueError):
            Location.objects.create(state="")

    def test_create_invalid_city_and_state_instance(self):
        with transaction.atomic():
            with self.assertRaises(ValueError):
                Location.objects.create(city=1)

        with self.assertRaises(ValueError):
            Location.objects.create(state=1)

    def test_create_invalid_city_and_state_unique_together(self):
        city = City.objects.all().first()
        state = State.objects.all().first()

        with self.assertRaises(IntegrityError):
            Location.objects.create(city=city, state=state)
            Location.objects.create(city=city, state=state)
