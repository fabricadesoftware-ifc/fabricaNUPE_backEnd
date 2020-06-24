from datetime import date

from nupe.core.models import Person
from resources.const.datas.Person import BIRTHDAY_DATE, CPF, FIRST_NAME, GENDER, LAST_NAME


def create_person(*, cpf: str = CPF, gender: chr = GENDER, birthday_date: date = BIRTHDAY_DATE) -> Person:
    return Person.objects.create(
        first_name=FIRST_NAME, last_name=LAST_NAME, cpf=cpf, gender=gender, birthday_date=birthday_date
    )
