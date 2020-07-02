from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

COURSE_MAX_LENGTH = 50
GRADE_MAX_LENGTH = 50


class Course(SafeDeleteModel):
    """
    Model para definir o nome de um curso

    Exemplo: 'Sistemas de Informação'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=COURSE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Grade(SafeDeleteModel):
    """
    Model para definir o nome de um grau de curso

    Exemplo: 'Bacharelado'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        name: nomenclatura
        courses: cursos que sejam desse grau (m2m)
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=GRADE_MAX_LENGTH, unique=True)
    courses = models.ManyToManyField(
        "Course", related_name="grades", related_query_name="grade", through="AcademicEducation"
    )

    def __str__(self):
        return self.name


class AcademicEducation(SafeDeleteModel):
    """
    Model para definir uma formação acadêmica de um aluno. É uma associativa entre a model de Course e Grade

    Exemplo: 'Bacharelado em Sistemas de Informação'

    Args:
        SafeDeleteModel: model responsável por mascarar o objeto ao invés de excluir do banco de dados

    Attr:
        course: objeto do tipo model 'Course' (o2m)
        grade: objeto do tipo model 'Grade' (o2m)
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    course = models.ForeignKey(
        "Course",
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.CASCADE,
    )
    grade = models.ForeignKey(
        "Grade",
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ["grade", "course"]

    def __str__(self):
        return f"{self.grade} em {self.course}"
