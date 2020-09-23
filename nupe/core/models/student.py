from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.regex import ONLY_NUMBERS

STUDENT_REGISTRATION_MAX_LENGTH = 35
RESPONSIBLE_MIN_AGE = 18


class Student(SafeDeleteModel):
    """
    Define as informações a respeito de um estudante

    Exemplo:
        'Luis Guerreiro - 202008010001'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        _academic_education_campus_deleted_id: identificador para restaurar a remoção (undelete)

        registration: número de matrícula do estudante

        person: objeto do tipo model 'Person' com as informações pessoais do estudante (o2m)

        academic_education_campus: objeto do tipo model 'AcademicEducationCampus' com a formação acadêmica/campus
        do estudante (o2m)

        responsibles_persons: pessoas responsáveis pelo estudante (m2m)

        graduated: status se o estudante já é formado ou não

        ingress_date: data de ingresso do estudante no campus

        updated_at: data da última atualização dos dados do estudante

        responsibles: relação inversa para a model Responsible

    Properties
        age: idade do estudante

        academic_education: nome do curso que o estudante participa
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados
    _academic_education_campus_deleted_id = models.IntegerField(default=None, null=True, blank=True)

    registration = models.CharField(max_length=STUDENT_REGISTRATION_MAX_LENGTH, validators=[ONLY_NUMBERS], unique=True)
    person = models.ForeignKey(
        "Person",
        related_name="student_registrations",
        related_query_name="student_registration",
        on_delete=models.CASCADE,
    )
    academic_education_campus = models.ForeignKey(
        "AcademicEducationCampus",
        related_name="students",
        related_query_name="student",
        on_delete=models.SET_NULL,
        null=True,
    )
    responsibles_persons = models.ManyToManyField(
        "Person", related_name="dependents", related_query_name="dependent", through="Responsible"
    )
    graduated = models.BooleanField(default=False)
    ingress_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["person", "academic_education_campus"]

    def __str__(self):
        return f"{self.person} - {self.registration}"

    @property
    def age(self):
        return self.person.age

    @property
    def academic_education(self):
        return str(self.academic_education_campus.academic_education)


class Responsible(SafeDeleteModel):
    """
    Define os responsáveis de um estudante caso seja menor de idade. É uma associativa entre Student e Person

    Exemplo:
        'João responsável pelo Luis Guerreiro'

    Atributos:
        student: objeto do tipo model 'Student'

        person: objeto do tipo model 'Person'
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    student = models.ForeignKey(
        "Student", related_name="responsibles", related_query_name="responsible", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "Person", related_name="responsibles", related_query_name="responsible", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["student", "person"]

    def __str__(self):
        return f"{self.person} responsável de {self.student.person}"
