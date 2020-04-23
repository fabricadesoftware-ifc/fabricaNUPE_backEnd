from django.db import models

CITY_MAX_LENGTH = 50
STATE_MAX_LENGTH = 50


class City(models.Model):
    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True, verbose_name="nome")

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=STATE_MAX_LENGTH, unique=True, verbose_name="nome")
    cities = models.ManyToManyField(
        City, related_name="states", related_query_name="state", through="Location", verbose_name="cidades"
    )

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.ForeignKey(
        City, related_name="locations", related_query_name="location", on_delete=models.PROTECT, verbose_name="cidade"
    )
    state = models.ForeignKey(
        State, related_name="locations", related_query_name="location", on_delete=models.PROTECT, verbose_name="estado"
    )

    class Meta:
        unique_together = ["city", "state"]
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def __str__(self):
        return "{} - {}".format(self.city, self.state)
