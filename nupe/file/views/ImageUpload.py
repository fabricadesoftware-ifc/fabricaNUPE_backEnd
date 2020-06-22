from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from nupe.file.models import ProfileImage
from nupe.file.serializers import ProfileImageCreateSerializer


class ProfileImageViewSet(GenericViewSet, CreateModelMixin):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageCreateSerializer
    parser_classes = [MultiPartParser]
