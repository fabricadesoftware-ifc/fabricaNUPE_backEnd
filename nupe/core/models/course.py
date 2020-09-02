from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

COURSE_MAX_LENGTH = 50
GRADE_MAX_LENGTH = 50


class Course(SafeDeleteModel):
    """
    Define o nome de um curso da instituição

    Exemplo:
        'Sistemas de Informação'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        name: nome do curso

        grades: relação inversa para a model Grade

        academic_education: relação inversa para a model AcademicEducation
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    name = models.CharField(max_length=COURSE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Grade(SafeDeleteModel):
    """
    Define o nível/grau de um curso

    Exemplo:
        'Bacharelado'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        name: nomenclatura do grau

        courses: cursos que pertencem a esse grau (m2m)

        academic_education: relação inversa para a model AcademicEducation
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
    Define uma formação acadêmica. É uma associativa entre a model de Course e Grade

    Exemplo:
        'Bacharelado em Sistemas de Informação'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        course: objeto do tipo model 'Course' (o2m)

        grade: objeto do tipo model 'Grade' (o2m)

        campus: relação inversa para a model Campus

        courses_campus: relação inversa para a model AcademicEducationCampus
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    course = models.ForeignKey("Course", related_name="academic_education", on_delete=models.CASCADE,)
    grade = models.ForeignKey("Grade", related_name="academic_education", on_delete=models.CASCADE,)

    class Meta:
        unique_together = ["grade", "course"]

    def __str__(self):
        return f"{self.grade} em {self.course}"
