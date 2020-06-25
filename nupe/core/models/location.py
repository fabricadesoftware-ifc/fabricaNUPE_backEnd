from django.db import models
from safedelete.models import NO_DELETE, SafeDeleteModel

CITY_MAX_LENGTH = 50
STATE_MAX_LENGTH = 50


class City(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class State(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    name = models.CharField(max_length=STATE_MAX_LENGTH, unique=True)
    cities = models.ManyToManyField("City", related_name="states", related_query_name="state", through="Location")

    def __str__(self):
        return self.name


class Location(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    city = models.ForeignKey(
        "City", related_name="locations", related_query_name="location", on_delete=models.PROTECT,
    )
    state = models.ForeignKey(
        "State", related_name="locations", related_query_name="location", on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ["city", "state"]

    def __str__(self):
        return f"{self.city} - {self.state}"
