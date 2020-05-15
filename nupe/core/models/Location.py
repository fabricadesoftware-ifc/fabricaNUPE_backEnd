from django.db import models

CITY_MAX_LENGTH = 50
STATE_MAX_LENGTH = 50


class City(models.Model):
    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class State(models.Model):
    name = models.CharField(max_length=STATE_MAX_LENGTH, unique=True)
    cities = models.ManyToManyField("City", related_name="states", related_query_name="state", through="Location")

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class Location(models.Model):
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
