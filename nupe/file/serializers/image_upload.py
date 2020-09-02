from rest_framework.serializers import CharField, ModelSerializer

from nupe.file.models import ProfileImage


class ProfileImageCreateSerializer(ModelSerializer):
    """
    Recebe e valida as informações para então cadastrar ou atualizar uma foto de perfil

    Campos:
        id: identificador (somente leitura)

        image: objeto do tipo ImageField responsável por gerenciar o arquivo de imagem

        url: url para visualizar a imagem (somente leitura)

    """

    url = CharField(source="image.url", read_only=True)

    class Meta:
        model = ProfileImage
        fields = [
            "id",
            "image",
            "url",
        ]
        extra_kwargs = {"image": {"write_only": True}}
