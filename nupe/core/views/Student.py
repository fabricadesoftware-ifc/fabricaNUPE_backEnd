from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from nupe.core.exceptions import ActionNotImplemented
from nupe.core.models import Student
from nupe.core.serializers import StudentCreateSerializer, StudentDetailSerializer, StudentListSerializer


class StudentViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    perms_map_action = {
        "list": ["core.view_student"],
        "retrieve": ["core.view_student"],
        "create": ["core.add_student"],
        "partial_update": ["core.change_student"],
        "destroy": ["core.delete_student"],
    }
    per_action_serializer = {
        "list": StudentListSerializer,
        "retrieve": StudentDetailSerializer,
        "create": StudentCreateSerializer,
        "partial_update": StudentCreateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.per_action_serializer.get(self.action)

        if serializer is None:
            raise ActionNotImplemented

        return serializer
