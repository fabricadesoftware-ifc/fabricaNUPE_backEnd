from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from nupe.core.exceptions import ActionNotImplemented
from nupe.core.models import Person
from nupe.core.serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer


class PersonViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Person.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    perms_map_action = {
        "list": ["core.view_person"],
        "retrieve": ["core.view_person"],
        "create": ["core.add_person"],
        "partial_update": ["core.change_person"],
        "destroy": ["core.delete_person"],
    }
    per_action_serializer = {
        "list": PersonListSerializer,
        "retrieve": PersonDetailSerializer,
        "create": PersonCreateSerializer,
        "partial_update": PersonCreateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.per_action_serializer.get(self.action)

        if serializer is None:
            raise ActionNotImplemented

        return serializer
