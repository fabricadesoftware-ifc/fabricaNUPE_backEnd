from rest_framework.serializers import CharField, ModelSerializer

from nupe.file.models import ProfileImage


class ProfileImageCreateSerializer(ModelSerializer):
    """
    Atributos a serem serializados para upload de uma imagem
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
