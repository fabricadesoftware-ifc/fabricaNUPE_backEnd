from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, ValidationError

from nupe.core.models import Person, Student
from nupe.core.models.student import Responsible
from nupe.core.serializers import PersonDetailSerializer, PersonListSerializer
from nupe.resources.messages.person import (
    SELF_RESPONSIBLE_MESSAGE,
    UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE,
    UNDER_AGE_RESPONSIBLE_MESSAGE,
)


class StudentListSerializer(ModelSerializer):
    """
    Retorna uma lista de estudantes cadastrados no banco de dados

    Campos:
        id: identificador (somente leitura)

        registration: número da matrícula

        full_name: nome completo

        ingress_date: data de ingresso na formação acadêmica

        graduated: status da formação acadêmica, se já se formou ou não
    """

    full_name = CharField(source="person.full_name")

    class Meta:
        model = Student
        fields = ["id", "registration", "full_name", "ingress_date", "graduated"]


class StudentDetailSerializer(ModelSerializer):
    """
    Retorna os detalhes de um estudante específico

    Campos:
        id: identificador (somente leitura)

        registration: número da matrícula

        personal_info: informações pessoais, as mesmas informações de PersonDetailSerializer

        academic_education: nome da formação acadêmica que está cursando

        institution: 'Instituição - Campus' onde estuda

        academic_education_campus: identificador do objeto da model AcademicEducationCampus

        responsibles: responsáveis do estudante

        ingress_date: data de ingresso na formação acadêmica

        graduated: status da formação acadêmica, se já se formou ou não
    """

    personal_info = PersonDetailSerializer(source="person")
    campus = CharField(source="academic_education_campus.campus")
    responsibles = PersonListSerializer(source="responsibles_persons", many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "registration",
            "personal_info",
            "academic_education",
            "campus",
            "academic_education_campus",
            "responsibles",
            "ingress_date",
            "graduated",
        ]


class StudentCreateSerializer(ModelSerializer):
    """
    Recebe e valida as informações para então cadastrar ou atualizar um estudante

    Campos:
        id: identificador (somente leitura)

        registration: número da matrícula

        person: identificador do objeto da model Person

        academic_education_campus: identificador do objeto da model AcademicEducationCampus

        responsibles: lista de id das pessoas responsáveis

        ingress_date: data de ingresso na formação acadêmica
    """

    responsibles = PrimaryKeyRelatedField(
        source="responsibles_persons", queryset=Person.objects.all(), many=True, required=False
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "registration",
            "person",
            "academic_education_campus",
            "responsibles",
            "ingress_date",
        ]

    def validate(self, data):
        """
        Verifica se os responsáveis do estudante são válidos

        Validações:
            Estudante menor de idade:
                Deve conter pelo menos um responsável

                Não deve ser o responsável de sí

                Não deve conter nenhum responsável menor de idade

        Argumentos:
            data (dict): dados enviados no body da requisição

        Retorna:
            [dict]: retorna os dados recebidos
        """
        # caso o atributo não seja informado, é utilizado a instancia de 'Student' para obte-lo
        # dessa forma a validação funcionará para as actions de 'create' e 'partial_update'
        person_data = data.get("person", self.instance.person if self.instance else None)

        responsibles_data = data.get("responsibles_persons", [])

        self.__verify_responsibles_of_under_age_student(responsibles=responsibles_data, person=person_data)

        return data

    def __verify_responsibles_of_under_age_student(self, *, responsibles: list, person: Person):
        """
        Verifica se os responsáveis do estudante são válidos

        Argumentos:
            responsibles (list): lista dos responsáveis do estudante
            person (Person): objeto da model Person

        Raises:
            ValidationError 1: caso o estudante seja menor de idade, ele deve conter pelo menos um responsável
            ValidationError 2: caso o estudante seja menor de idade, ele não deve ser o responsável de sí
            ValidationError 3: caso o estudante seja menor de idade, não deve conter nenhum responsável menor de idade
        """
        student_is_under_age = person.age < Responsible.MINIMUM_AGE

        # ValidationError 1
        if student_is_under_age and not responsibles:
            raise ValidationError({"responsibles": UNDER_AGE_REQUIRED_RESPONSIBLE_MESSAGE})

        for responsible in responsibles:
            responsible_is_under_age = responsible.age < Responsible.MINIMUM_AGE
            student_is_self_responsible = responsible.id == person.id

            # ValidationError 2
            if student_is_under_age and student_is_self_responsible:
                raise ValidationError({"responsibles": SELF_RESPONSIBLE_MESSAGE})

            # ValidationError 3
            elif responsible_is_under_age:
                raise ValidationError({"responsibles": UNDER_AGE_RESPONSIBLE_MESSAGE})
