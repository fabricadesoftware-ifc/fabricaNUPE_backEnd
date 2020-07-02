from django.db import models
from safedelete.models import NO_DELETE, SafeDeleteModel

CITY_MAX_LENGTH = 50
STATE_MAX_LENGTH = 50


class City(SafeDeleteModel):
    """
    Model para definir o nome de uma cidade

    Exemplo: 'Araquari'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class State(SafeDeleteModel):
    """
    Model para definir o nome de um estado

    Exemplo: 'Santa Catarina'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
        cities: cidades desse estado (m2m)
    """

    _safedelete_policy = NO_DELETE  # não remove e nem mascara o objeto

    name = models.CharField(max_length=STATE_MAX_LENGTH, unique=True)
    cities = models.ManyToManyField("City", related_name="states", related_query_name="state", through="Location")

    def __str__(self):
        return self.name


class Location(SafeDeleteModel):
    """
    Model para definir uma cidade pertencente à um estado. É uma associativa entre a model de City e State

    Exemplo: 'Araquari - Santa Catarina'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        city: objeto do tipo model 'City' (o2m)
        state: objeto do tipo model 'State' (o2m)
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

    def __str__(self):
        return f"{self.city} - {self.state}"
