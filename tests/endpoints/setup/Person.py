from nupe.core.models import Person
from tests.models.Person import BIRTHDAY_DATE, CPF, FIRST_NAME, GENDER, LAST_NAME, RG


def create_person(*, cpf: str = CPF, rg: str = RG) -> Person:
    return Person.objects.create(
        first_name=FIRST_NAME, last_name=LAST_NAME, cpf=cpf, rg=rg, gender=GENDER, birthday_date=BIRTHDAY_DATE
    )
