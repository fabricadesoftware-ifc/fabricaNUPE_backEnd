from rest_framework.serializers import CharField, ModelSerializer, ValidationError
from validate_docbr import CPF

from nupe.core.models import Person
from nupe.file.services.image_upload import ProfileImageService
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

    profile_image = CharField(source="profile_image.image.url", default=None)

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
            "profile_image",
        ]


class PersonCreateSerializer(ModelSerializer):
    """
    Atributos a serem serializados para criação de uma pessoa
    """

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "cpf", "birthday_date", "gender", "contact", "profile_image"]

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

    def update(self, instance, validated_data):
        profile_image_service = ProfileImageService()

        # exclui a imagem de perfil antiga
        profile_image_service.remove_file(instance.profile_image)

        return super().update(instance, validated_data)
