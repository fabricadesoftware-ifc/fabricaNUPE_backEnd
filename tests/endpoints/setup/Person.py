from nupe.core.models import Person

FIRST_NAME = "luis"
LAST_NAME = "guerreiro"
CPF = "27766309050"
RG = "1234567"
GENDER = "M"
BIRTHDAY_DATE = "1999-02-14"


class SetupPerson:
    @staticmethod
    def create_person() -> Person:
        return Person.objects.create(
            first_name=FIRST_NAME, last_name=LAST_NAME, cpf=CPF, rg=RG, gender=GENDER, birthday_date=BIRTHDAY_DATE
        )
