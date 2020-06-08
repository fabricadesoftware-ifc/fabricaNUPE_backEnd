from nupe.core.models import City, Location, State
from resources.const.datas.Location import CITY_NAME, STATE_NAME


def create_location(*, city_name=CITY_NAME, state_name=STATE_NAME):
    city = City.objects.create(name=city_name)
    state = State.objects.create(name=state_name)

    return Location.objects.create(city=city, state=state)
