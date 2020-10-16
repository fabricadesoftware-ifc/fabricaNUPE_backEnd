from rest_framework.viewsets import ModelViewSet

from nupe.core.filters import StudentFilter
from nupe.core.models import Student
from nupe.core.serializers import StudentCreateSerializer, StudentDetailSerializer, StudentListSerializer


class StudentViewSet(ModelViewSet):
    """
    list: retorna todos os estudantes do banco de dados. RF.SIS.042, RF.SIS.043, RF.SIS.044, RF.SIS.045

    retrieve: retorna um estudante especifico do banco de dados. RF.SIS.046, RF.SIS.047, RF.SIS.048

    create: cadastra um estudante no banco de dados. RF.SIS.041

    destroy: exclui um estudante do banco de dados. RF.SIS.050

    partial_update: atualiza um ou mais atributos de um estudante. RF.SIS.049
    """

    queryset = Student.objects.all()
    lookup_field = "registration"
    filterset_class = StudentFilter
    search_fields = ["person__first_name", "person__last_name"]  # RF.SIS.044
    ordering_fields = ["registration", "person__first_name", "person__last_name"]  # RF.SIS.045
    ordering = ["person__first_name", "person__last_name"]

    per_action_serializer = {
        "list": StudentListSerializer,
        "retrieve": StudentDetailSerializer,
        "create": StudentCreateSerializer,
        "partial_update": StudentCreateSerializer,
    }

    http_method_names = ["get", "post", "patch", "delete"]

    perms_map_action = {
        "list": ["core.view_student"],
        "retrieve": ["core.view_student"],
        "create": ["core.add_student"],
        "partial_update": ["core.change_student"],
        "destroy": ["core.delete_student"],
    }

    def get_serializer_class(self):
        return self.per_action_serializer.get(self.action)
