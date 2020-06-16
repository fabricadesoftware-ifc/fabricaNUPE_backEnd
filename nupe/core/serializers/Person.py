from rest_framework.serializers import ModelSerializer, ValidationError
from validate_docbr import CPF

from nupe.core.models import Person
from resources.const.messages.Person import PERSON_INVALID_CPF_MESSAGE


class PersonListSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "full_name", "contact"]


class PersonDetailSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "cpf",
            "rg",
            "birthday_date",
            "gender",
            "contact",
        ]


class PersonCreateSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "cpf", "rg", "birthday_date", "gender", "contact"]
        read_only_fields = ["id"]

    def validate_cpf(self, cpf):
        if not CPF().validate(cpf):
            raise ValidationError(PERSON_INVALID_CPF_MESSAGE)

        return cpf
