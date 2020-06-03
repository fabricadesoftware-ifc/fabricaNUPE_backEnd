from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField

from nupe.core.models import Person, Student
from nupe.core.serializers import PersonDetailSerializer, PersonListSerializer


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
