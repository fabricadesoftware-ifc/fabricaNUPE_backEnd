from rest_framework.viewsets import ModelViewSet

from nupe.core.exceptions import ActionNotImplemented
from nupe.core.filters import PersonFilter
from nupe.core.models import Person
from nupe.core.serializers import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    lookup_field = "cpf"
    filterset_class = PersonFilter
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]
    ordering = ["first_name", "last_name"]

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
        """
        Se a ação utilizada conter um serializer associado, ele será retornado.
        Caso contrário é emitido uma exceção informativa
        """

        serializer = self.per_action_serializer.get(self.action)

        if serializer is None:
            raise ActionNotImplemented

        return serializer
