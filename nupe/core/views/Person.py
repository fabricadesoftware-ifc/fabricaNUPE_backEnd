from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from nupe.core.exceptions import ActionHasNoSerializer
from nupe.core.models import Person
from nupe.core.serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer


class PersonViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Person.objects.all()
    perms_map_action = {
        "list": ["core.view_person"],
        "retrieve": ["core.view_person"],
        "create": ["core.add_person"],
        "update": ["core.change_person"],
    }
    per_action_serializer = {
        "list": PersonListSerializer,
        "retrieve": PersonDetailSerializer,
        "create": PersonCreateSerializer,
        "update": PersonCreateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.per_action_serializer.get(self.action)

        if serializer is None:
            raise ActionHasNoSerializer

        return serializer
