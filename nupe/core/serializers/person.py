from rest_framework.serializers import ModelSerializer, ValidationError
from validate_docbr import CPF

from nupe.core.models import Person
from resources.const.messages.person import PERSON_INVALID_CPF_MESSAGE


class PersonListSerializer(ModelSerializer):
    """
    Atributos a serem exibidos na listagem de pessoa
    """

    class Meta:
        model = Person
        fields = ["id", "full_name", "cpf", "contact"]


class PersonDetailSerializer(ModelSerializer):
    """
    Atributos a serem exibidos no detalhamento de uma pessoa
    """

    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "cpf",
            "birthday_date",
            "gender",
            "contact",
        ]


class PersonCreateSerializer(ModelSerializer):
    """
    Atributos a serem serializados para criação de uma pessoa
    """

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "cpf", "birthday_date", "gender", "contact"]
        read_only_fields = ["id"]

    def validate_cpf(self, cpf):
        """
        Verifica se o cpf é válido com base no digito verificador

        Args:
            cpf (str): atributo do serializer data

        Raises:
            ValidationError: caso o cpf seja inválido

        Returns:
            [str]: retorna o cpf somente se for válido
        """
        if not CPF().validate(cpf):
            raise ValidationError(PERSON_INVALID_CPF_MESSAGE)

        return cpf
