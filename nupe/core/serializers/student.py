from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, ValidationError

from nupe.core.models import Person, Student
from nupe.core.models.student import RESPONSIBLE_MIN_AGE
from nupe.core.serializers import PersonDetailSerializer, PersonListSerializer
from resources.const.messages.responsible import (
    SELF_RESPONSIBLE_MESSAGE,
    UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE,
    UNDER_AGE_RESPONSIBLE_MESSAGE,
)


class StudentListSerializer(ModelSerializer):
    """
    Atributos a serem exibidos na listagem de estudante
    """

    full_name = CharField(source="person.full_name")

    class Meta:
        model = Student
        fields = ["id", "registration", "full_name", "ingress_date", "graduated"]


class StudentDetailSerializer(ModelSerializer):
    """
    Atributos a serem exibidos no detalhamento de um estudante
    """

    personal_info = PersonDetailSerializer(source="person")
    course = CharField(source="academic_education_campus.academic_education")
    campus = CharField(source="academic_education_campus.campus")
    responsibles = PersonListSerializer(source="responsibles_persons", many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "registration",
            "personal_info",
            "course",
            "campus",
            "academic_education_campus_id",
            "responsibles",
            "ingress_date",
            "graduated",
        ]


class StudentCreateSerializer(ModelSerializer):
    """
    Atributos a serem serializados para criação de um estudante
    """

    responsibles = PrimaryKeyRelatedField(source="responsibles_persons", many=True, queryset=Person.objects.all())

    class Meta:
        model = Student
        fields = ["id", "registration", "person", "academic_education_campus", "responsibles", "ingress_date"]
        read_only_fields = ["id"]

    def validate(self, data):
        # caso o atributo não seja informado, é utilizado a instancia de 'Student' para obte-lo
        # dessa forma a validação funcionará para as actions de 'create' e 'partial_update'
        person_data = data.get("person", self.instance.person if self.instance else None)
        responsibles_data = data.get("responsibles_persons", [])

        if person_data:
            self.__verify_responsibles_of_under_age_student(responsibles=responsibles_data, person=person_data)

        return data

    def __verify_responsibles_of_under_age_student(self, *, responsibles: list, person: Person):
        """
        Verifica se os responsáveis do estudante são válidos

        Args:
            responsibles (list): lista dos responsáveis do estudante
            person (Person): informações pessoais do estudante

        Raises:
            ValidationError 1: caso o estudante seja menor de idade, ele deve conter pelo menos um responsável
            ValidationError 2: caso o estudante seja menor de idade, ele não deve ser o responsável de sí
            ValidationError 3: caso o estudante seja menor de idade, não deve conter nenhum responsável menor de idade
        """
        student_is_under_age = person.age < RESPONSIBLE_MIN_AGE

        # ValidationError 1
        if student_is_under_age and not responsibles:
            raise ValidationError({"responsibles": UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE})

        for responsible in responsibles:
            responsible_is_under_age = responsible.age < RESPONSIBLE_MIN_AGE
            student_is_self_responsible = responsible.id == person.id

            # ValidationError 2
            if student_is_under_age and student_is_self_responsible:
                raise ValidationError({"responsibles": SELF_RESPONSIBLE_MESSAGE})

            # ValidationError 3
            elif responsible_is_under_age:
                raise ValidationError({"responsibles": UNDER_AGE_RESPONSIBLE_MESSAGE})
