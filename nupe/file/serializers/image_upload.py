from rest_framework.serializers import ModelSerializer

from nupe.file.models import ProfileImage


class ProfileImageCreateSerializer(ModelSerializer):
    """
    Recebe e valida as informações para então fazer o upload da foto de perfil

    Campos:
        id: identificador (somente leitura)

        image: objeto do tipo ImageField responsável por gerenciar o arquivo de imagem

        attachment_id: identificador para fazer associação com outro objeto (somente leitura)

        uploaded_at: data/hora do upload (somente leitura)

    """

    class Meta:
        model = ProfileImage
        fields = ["id", "image", "attachment_id", "uploaded_at"]
        read_only_fields = ["attachment_id", "uploaded_at"]
        extra_kwargs = {"image": {"write_only": True}}
