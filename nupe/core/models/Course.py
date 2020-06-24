from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

COURSE_MAX_LENGTH = 50
GRADE_MAX_LENGTH = 50


class Course(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=COURSE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Grade(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=GRADE_MAX_LENGTH, unique=True)
    courses = models.ManyToManyField(
        "Course", related_name="grades", related_query_name="grade", through="AcademicEducation"
    )

    def __str__(self):
        return self.name


class AcademicEducation(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

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
