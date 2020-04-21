from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import City, Location, State


class CityTestCase(TestCase):
    city = "Joinville"

    def test_create_city_valid(self):
        city = City.objects.create(name=self.city)
        self.assertEqual(city.name, self.city)

    def test_create_city_invalid(self):
        # test max_length
        with self.assertRaises(ValidationError):
            City.objects.create(name=self.city * 50).clean_fields()

        # test unique name
        City.objects.create(name=self.city)
        with self.assertRaises(IntegrityError):
            City.objects.create(name=self.city)


class StateTestCase(TestCase):
    state = "Santa Catarina"

    def test_create_state_valid(self):
        state = State.objects.create(name=self.state)
        self.assertEqual(state.name, self.state)

    def test_create_state_invalid(self):
        # test max_length
        with self.assertRaises(ValidationError):
            State.objects.create(name=self.state * 50).clean_fields()

        # test unique name
        State.objects.create(name=self.state)
        with self.assertRaises(IntegrityError):
            State.objects.create(name=self.state)


class LocationTestCase(TestCase):
    city = "Joinville"
    state = "Santa Catarina"

    def setUp(self):
        City.objects.create(name=self.city)
        State.objects.create(name=self.state)

    def test_create_location_valid(self):
        city = City.objects.get(name=self.city)
        state = State.objects.get(name=self.state)

        location = Location.objects.create(city=city, state=state)

        self.assertEqual(location.city.name, self.city)
        self.assertEqual(location.state.name, self.state)
        self.assertEqual(Location.objects.all().count(), 1)

    def test_create_unique_together_location_invalid(self):
        city = City.objects.get(name=self.city)
        state = State.objects.get(name=self.state)

        Location.objects.create(city=city, state=state)

        # test unique together
        with self.assertRaises(IntegrityError):
            Location.objects.create(city=city, state=state)

        # test instance
        with self.assertRaises(ValueError):
            Location.objects.create(city=1, state=1)
