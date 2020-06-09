from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, ValidationError

from nupe.core.models import Person, Student
from nupe.core.models.Student import RESPONSIBLE_MIN_AGE
from nupe.core.serializers import PersonDetailSerializer, PersonListSerializer
from resources.const.messages.Responsible import UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE


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
        person = data.get("person")
        responsibles = data.get("responsibles_persons")

        if person:
            if person.age < RESPONSIBLE_MIN_AGE and not responsibles:
                raise ValidationError({"responsibles_persons": UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE})

        return data
