from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, ValidationError

from nupe.core.models import Person, Student
from nupe.core.models.Student import RESPONSIBLE_MIN_AGE
from nupe.core.serializers import PersonDetailSerializer, PersonListSerializer
from resources.const.messages.Responsible import (
    MYSELF_RESPONSIBLE_MESSAGE,
    UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE,
    UNDER_AGE_RESPONSIBLE_MESSAGE,
)


class StudentListSerializer(ModelSerializer):
    full_name = CharField(source="person.full_name")

    class Meta:
        model = Student
        fields = ["id", "registration", "full_name", "ingress_date", "graduated"]


class StudentDetailSerializer(ModelSerializer):
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
    responsibles_persons = PrimaryKeyRelatedField(many=True, queryset=Person.objects.all())

    class Meta:
        model = Student
        fields = ["id", "registration", "person", "academic_education_campus", "responsibles_persons", "ingress_date"]
        read_only_fields = ["id"]

    def validate(self, data):
        person_data = data.get("person")
        responsibles_data = data.get("responsibles_persons")

        # caso "person" não seja informado no data, é utilizado a instancia de student object para obter "person"
        # dessa forma a validação funcionará para as actions de "create" e "partial_update"
        person = person_data if person_data else self.instance.person

        if person and person.age < RESPONSIBLE_MIN_AGE:
            self.__verify_responsibles_of_under_age_student(responsibles=responsibles_data, person=person)

        return data

    def __verify_responsibles_of_under_age_student(self, *, responsibles: list, person: Person) -> ValidationError:
        """Validações para estudantes menor de idade"""

        if not responsibles:
            # Deve conter pelo menos 1 responsável
            raise ValidationError({"responsibles_persons": UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE})

        for responsible in responsibles:
            if responsible.id == person.id:
                # O estudante não pode ser o próprio responsável
                raise ValidationError({"responsibles_persons": MYSELF_RESPONSIBLE_MESSAGE})

            elif responsible.age < RESPONSIBLE_MIN_AGE:
                # O responsável não pode ser menor de idade
                raise ValidationError({"responsibles_persons": UNDER_AGE_RESPONSIBLE_MESSAGE})
