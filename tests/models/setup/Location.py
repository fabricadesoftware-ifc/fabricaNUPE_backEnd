from nupe.core.models import City, Location, State


def setup_create_location(*, city_name, state_name):
    city = City.objects.create(name=city_name)
    state = State.objects.create(name=state_name)

    return Location.objects.create(city=city, state=state)
