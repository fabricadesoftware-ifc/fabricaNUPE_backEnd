from rest_framework.serializers import CharField, ModelSerializer, SlugRelatedField, ValidationError
from validate_docbr import CPF

from uploader.models import Image
from uploader.serializers import ImageSerializer

from nupe.core.models import Person
# from nupe.file.models import ProfileImage
from nupe.resources.messages.person import PERSON_INVALID_CPF_MESSAGE


class PersonListSerializer(ModelSerializer):
    """
    Retorna uma lista de pessoas cadastradas no banco de dados

    Campos:
        id: identificador (somente leitura)

        full_name: nome completo

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        contact: número do telefone
    """

    class Meta:
        model = Person
        fields = ["id", "full_name", "cpf", "contact"]


class PersonDetailSerializer(ModelSerializer):
    # capa = ImageSerializer(required=False)
    """
    Retorna os detalhes de uma pessoa específica

    Campos:
        id: identificador (somente leitura)

        first_name: nome

        last_name: sobrenome

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        birthday_date: data de nascimento

        gender: sexo

        contact: número do telefone

        profile_image: url da foto de perfil
    """

    # profile_image = CharField(source="profile_image.url", default=None)

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
    profile_image_attachment_key = SlugRelatedField(
        source="profile image",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    profile_image = ImageSerializer(
        required=False,
        read_only=True
    )
    
    """
    Recebe e valida as informações para então cadastrar ou atualizar uma pessoa

    Campos:
        id: identificador (somente leitura)

        first_name: nome

        last_name: sobrenome

        cpf: número do documento 'Cadastro de Pessoas Físicas'

        birthday_date: data de nascimento

        gender: sexo

        contact: número do telefone

        profile_image: atributo 'attachment_id' da model ProfileImage (necessário fazer upload da imagem antes
        para obter o identificador de associação)
    """

    # profile_image = SlugRelatedField(slug_field="attachment_id", queryset=ProfileImage.objects.all(), required=False)

    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name", "cpf", "birthday_date", "gender", "contact", "profile_image"]

    def validate_cpf(self, cpf):
        """
        Verifica se o cpf é válido

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

            validated_data (dict): dados já validados para atualização
        """
        new_profile_image = validated_data.get("profile_image")

        if new_profile_image is not None:
            # exclui a imagem de perfil antiga
            instance.profile_image.delete()

        return super().update(instance, validated_data)
