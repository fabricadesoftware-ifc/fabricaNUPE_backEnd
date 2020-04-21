from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cities = models.ManyToManyField(City, related_name="states", related_query_name="state", through="Location")

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.ForeignKey(City, related_name="locations", related_query_name="location", on_delete=models.PROTECT)
    state = models.ForeignKey(State, related_name="locations", related_query_name="location", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["city", "state"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return "{} - {}".format(self.city, self.state)
