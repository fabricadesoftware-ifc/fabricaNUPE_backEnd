from django.db import models
from safedelete.models import NO_DELETE, SafeDeleteModel

CITY_MAX_LENGTH = 50
STATE_MAX_LENGTH = 50
INITIALS_STATE_MAX_LENGTH = 2


class City(SafeDeleteModel):
    """
    Define o nome de uma cidade

    Exemplo:
        'Araquari'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome

        states: relação inversa para a model State
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True)

    def __str__(self) -> str:
        return self.name


class State(SafeDeleteModel):
    """
    Define o nome de um estado

    Exemplo:
        'Santa Catarina'

    Atributos:
        _safedelete_policy: NO_DELETE

        name: nome

        initials: sigla

        cities: cidades pertencente à esse estado (m2m)
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=STATE_MAX_LENGTH, unique=True)
    initials = models.CharField(max_length=INITIALS_STATE_MAX_LENGTH, unique=True)
    cities = models.ManyToManyField("City", related_name="states", related_query_name="state", through="Location")

    def __str__(self) -> str:
        return self.name


class Location(SafeDeleteModel):
    """
    Define uma cidade pertencente à um estado. É uma associativa entre a model de City e State

    Exemplo:
        'Araquari - Santa Catarina'

    Atributos:
        _safedelete_policy: NO_DELETE

        city: objeto do tipo model 'City' (o2m)

        state: objeto do tipo model 'State' (o2m)

        campus: relação inversa para a model Campus
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    city = models.ForeignKey(
        "City", related_name="locations", related_query_name="location", on_delete=models.PROTECT,
    )
    state = models.ForeignKey(
        "State", related_name="locations", related_query_name="location", on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ["city", "state"]

    def __str__(self) -> str:
        return f"{self.city} - {self.state.initials}"
