from rest_framework.viewsets import ModelViewSet

from nupe.core.models import Campus, Institution
from nupe.core.serializers import CampusListSerializer, CampusSerializer, InstitutionSerializer


class InstitutionViewSet(ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    lookup_field = "name"

    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_institution"],
        "retrieve": ["core.view_institution"],
        "create": ["core.add_institution"],
        "partial_update": ["core.change_institution"],
        "destroy": ["core.delete_institution"],
    }


class CampusViewSet(ModelViewSet):
    queryset = Campus.objects.all()
    lookup_field = "name"

    ordering = "name"

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_campus"],
        "retrieve": ["core.view_campus"],
        "create": ["core.add_campus"],
        "partial_update": ["core.change_campus"],
        "destroy": ["core.delete_campus"],
    }

    per_action_serializer = {
        "list": CampusListSerializer,
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action, CampusSerializer)
