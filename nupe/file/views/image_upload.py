import os

from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from nupe.file.models import ProfileImage
from nupe.file.serializers import ProfileImageCreateSerializer


class ProfileImageViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageCreateSerializer
    parser_classes = [MultiPartParser]

    perms_map_action = {
        "create": ["file.add_profileimage"],
        "destroy": ["file.delete_profileimage"],
    }

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk:
            profile_image_path = get_object_or_404(ProfileImage, pk=pk).image.path
            os.remove(profile_image_path)

        return super().destroy(request, *args, **kwargs)
