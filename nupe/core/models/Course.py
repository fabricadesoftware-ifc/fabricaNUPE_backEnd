from django.db import models

COURSE_MAX_LENGTH = 50
GRADE_MAX_LENGTH = 50


class Course(models.Model):
    name = models.CharField(max_length=COURSE_MAX_LENGTH, unique=True, verbose_name="nome")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=GRADE_MAX_LENGTH, unique=True, verbose_name="nome")
    courses = models.ManyToManyField(
        Course, related_name="grades", related_query_name="grade", through="AcademicEducation", verbose_name="cursos"
    )

    class Meta:
        verbose_name = "Grau"
        verbose_name_plural = "Graus"

    def __str__(self):
        return self.name


class AcademicEducation(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.PROTECT,
        verbose_name="curso",
    )
    grade = models.ForeignKey(
        Grade,
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.PROTECT,
        verbose_name="grau",
    )

    class Meta:
        unique_together = ["grade", "course"]
        verbose_name = "Formação Acadêmica"
        verbose_name_plural = "Formações Acadêmicas"

    def __str__(self):
        return "{} em {}".format(self.grade, self.course)
