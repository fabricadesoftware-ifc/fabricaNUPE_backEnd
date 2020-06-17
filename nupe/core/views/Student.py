from rest_framework.viewsets import GenericViewSet, ModelViewSet

from nupe.core.exceptions import ActionNotImplemented
from nupe.core.filters import StudentFilter
from nupe.core.models import Student
from nupe.core.serializers import StudentCreateSerializer, StudentDetailSerializer, StudentListSerializer


class StudentViewSet(ModelViewSet, GenericViewSet):
    queryset = Student.objects.all()
    lookup_field = "registration"
    filterset_class = StudentFilter
    search_fields = ["person__first_name", "person__last_name"]
    ordering_fields = ["registration", "person__first_name", "person__last_name"]
    ordering = ["person__first_name", "person__last_name"]

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
