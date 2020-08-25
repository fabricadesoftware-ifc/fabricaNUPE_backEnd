from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from nupe.file.models import ProfileImage
from nupe.file.serializers import ProfileImageCreateSerializer

# TODO adicionar endpoint para atualizar a imagem de perfil


class ProfileImageViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    """
    create: upload a image into database

    delete: remove a image from database
    """

    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageCreateSerializer
    parser_classes = [MultiPartParser]

    perms_map_action = {
        "create": ["file.add_profileimage"],
        "destroy": ["file.delete_profileimage"],
    }
