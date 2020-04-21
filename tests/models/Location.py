from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import City, Location, State


class LocationTestCase(TestCase):
    city = "Joinville"
    state = "Santa Catarina"

    def setUp(self):
        City.objects.create(name=self.city)
        State.objects.create(name=self.state)

    def test_create_location(self):
        city = City.objects.get(name=self.city)
        state = State.objects.get(name=self.state)

        location = Location.objects.create(city=city, state=state)

        self.assertEqual(location.city.name, self.city)
        self.assertEqual(location.state.name, self.state)
        self.assertEqual(Location.objects.all().count(), 1)

    def test_create_unique_together_location(self):
        city = City.objects.get(name=self.city)
        state = State.objects.get(name=self.state)

        Location.objects.create(city=city, state=state)

        with self.assertRaises(IntegrityError):
            Location.objects.create(city=city, state=state)

        with self.assertRaises(ValueError):
            Location.objects.create(city=1, state=1)


# TODO test for city and state
