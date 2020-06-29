from nupe.core.models import City, Location, State
from resources.const.datas.location import CITY_NAME, STATE_NAME


def create_location(*, city_name: str = CITY_NAME, state_name: str = STATE_NAME):
    city, created = City.objects.get_or_create(name=city_name)
    state, created = State.objects.get_or_create(name=state_name)

    location, created = Location.objects.get_or_create(city=city, state=state)

    return location
