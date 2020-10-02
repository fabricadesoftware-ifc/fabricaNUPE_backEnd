from rest_framework.viewsets import ModelViewSet

from nupe.core.models import AttendanceReason, CrisisType, DrugType, SpecialNeedType
from nupe.core.serializers import (
    AttendanceCreateReasonSerializer,
    AttendanceReasonSerializer,
    CrisisTypeSerializer,
    DrugTypeSerializer,
    SpecialNeedTypeSerializer,
)


class SpecialNeedTypeViewSet(ModelViewSet):
    queryset = SpecialNeedType.objects.all()
    serializer_class = SpecialNeedTypeSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    perms_map_action = {
        "list": ["core.view_specialneedtype"],
        "retrieve": ["core.view_specialneedtype"],
        "create": ["core.add_specialneedtype"],
        "partial_update": ["core.change_specialneedtype"],
        "destroy": ["core.delete_specialneedtype"],
    }


class CrisisTypeViewSet(ModelViewSet):
    queryset = CrisisType.objects.all()
    serializer_class = CrisisTypeSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    perms_map_action = {
        "list": ["core.view_crisistype"],
        "retrieve": ["core.view_crisistype"],
        "create": ["core.add_crisistype"],
        "partial_update": ["core.change_crisistype"],
        "destroy": ["core.delete_crisistype"],
    }


class DrugTypeViewSet(ModelViewSet):
    queryset = DrugType.objects.all()
    serializer_class = DrugTypeSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    perms_map_action = {
        "list": ["core.view_drugtype"],
        "retrieve": ["core.view_drugtype"],
        "create": ["core.add_drugtype"],
        "partial_update": ["core.change_drugtype"],
        "destroy": ["core.delete_drugtype"],
    }


class AttendanceReasonViewSet(ModelViewSet):
    queryset = AttendanceReason.objects.all()
    serializer_class = AttendanceReasonSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_attendancereason"],
        "retrieve": ["core.view_attendancereason"],
        "create": ["core.add_attendancereason"],
        "partial_update": ["core.change_attendancereason"],
        "destroy": ["core.delete_attendancereason"],
    }

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return AttendanceCreateReasonSerializer

        return self.serializer_class
