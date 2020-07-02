from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.regex import ONLY_NUMBERS

STUDENT_REGISTRATION_MAX_LENGTH = 35
RESPONSIBLE_MIN_AGE = 18


class Student(SafeDeleteModel):
    """
    Model para definir as informações sobre um estudante

    Exemplo: 'Fulano de Tal - 202002071234'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        registration: número de matrícula
        person: objeto do tipo model 'Person' com as informações pessoais (o2m)
        academic_education_campus: objeto do tipo model 'AcademicEducationCampus' com o curso do campus (o2m)
        responsibles_persons: pessoas responsáveis pelo aluno (m2m)
        graduated: status se já se formou ou não
        ingress_date: data de ingresso
        updated_at: data de atualização

    Properties:
        age: idade
        academic_education: nome do curso
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
        "AcademicEducationCampus", related_name="students", on_delete=models.SET_NULL, null=True
    )
    responsibles_persons = models.ManyToManyField(
        "Person", related_name="dependents_students", related_query_name="dependent_student", through="Responsible"
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
    Model para definir os responsáveis de um aluno menor de idade. É uma associativa entre Student e Person

    Exemplo: 'Pai do Fulano de Tal responsável pelo Fulano de Tal'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
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
