from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import StudentFilter
from nupe.core.models import Student
from nupe.core.serializers import StudentCreateSerializer, StudentDetailSerializer, StudentListSerializer


class StudentViewSet(ModelViewSet):
    """
    list: retorna todos os estudantes do banco de dados

    retrieve: retorna um estudante especifico do banco de dados

    create: cadastra um estudante no banco de dados

    destroy: exclui um estudante do banco de dados

    partial_update: atualiza um ou mais atributos de um estudante
    """

    queryset = Student.objects.all()
    lookup_field = "registration"

    filterset_class = StudentFilter
    search_fields = ["person__first_name", "person__last_name"]
    ordering_fields = ["registration", "person__first_name", "person__last_name"]
    ordering = ["person__first_name", "person__last_name"]  # ordem padrão

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
        return self.per_action_serializer.get(self.action)
