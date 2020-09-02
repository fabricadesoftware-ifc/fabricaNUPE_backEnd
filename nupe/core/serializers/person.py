from rest_framework.serializers import CharField, ModelSerializer, ValidationError
from validate_docbr import CPF

from nupe.core.models import Person
from nupe.file.models import ProfileImage
from nupe.file.services.image_upload import ProfileImageService
from resources.const.messages.person import PERSON_INVALID_CPF_MESSAGE


class PersonListSerializer(ModelSerializer):
    """
    Retorna uma lista de pessoas cadastradas no banco de dados

    Campos:
        id: identificador

        full_name: nome completo

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        contact: número do telefone
    """

    class Meta:
        model = Person
        fields = ["id", "full_name", "cpf", "contact"]


class PersonDetailSerializer(ModelSerializer):
    """
    Retorna os detalhes de uma pessoa específica

    Campos:
        id: identificador

        first_name: nome

        last_name: sobrenome

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        birthday_date: data de nascimento

        gender: sexo

        contact: número do telefone

        profile_image: url da foto de perfil
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
    Recebe e valida as informações para então cadastrar uma nova pessoa

    Campos:
        id: identificador (somente leitura)

        first_name: nome

        last_name: sobrenome

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        birthday_date: data de nascimento

        gender: sexo

        contact: número do telefone

        profile_image: identificador da foto de perfil (necessário fazer upload da imagem antes, para obter o id)
    """

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "cpf", "birthday_date", "gender", "contact", "profile_image"]

    def validate_cpf(self, cpf):
        """
        Verifica se o cpf é válido com base no digito verificador

        Argumentos:
            cpf (str): atributo do serializer data

        Raises:
            ValidationError: caso o cpf seja inválido

        Retorna:
            str: retorna o cpf somente se for válido
        """
        if not CPF().validate(cpf):
            raise ValidationError(PERSON_INVALID_CPF_MESSAGE)

        return cpf

    def update(self, instance, validated_data):
        """
        Atualiza as informações de uma pessoa específica

        Argumentos:
            instance (Person): objeto da model Person a ser atualizado

            validated_data (dict): dados para atualização
        """
        new_profile_image_id = validated_data.get("profile_image")

        if new_profile_image_id is not None:
            try:
                new_profile_image_exists = ProfileImage.objects.get(pk=new_profile_image_id)

                updating_profile_image = new_profile_image_id != instance.profile_image.id

                if updating_profile_image and new_profile_image_exists:
                    profile_image_service = ProfileImageService()

                    # exclui a imagem de perfil antiga
                    profile_image_service.remove_file(profile_image=instance.profile_image)

            except ProfileImage.DoesNotExist:
                # se o id informado não existir no banco de dados a foto de perfil não é atualizada
                del validated_data["profile_image"]

        return super().update(instance, validated_data)
