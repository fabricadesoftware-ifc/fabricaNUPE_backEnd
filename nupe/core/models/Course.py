from django.db import models

COURSE_MAX_LENGTH = 50
GRADE_MAX_LENGTH = 50


class Course(models.Model):
    name = models.CharField(max_length=COURSE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class Grade(models.Model):
    name = models.CharField(max_length=GRADE_MAX_LENGTH, unique=True)
    courses = models.ManyToManyField(
        "Course", related_name="grades", related_query_name="grade", through="AcademicEducation"
    )

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class AcademicEducation(models.Model):
    course = models.ForeignKey(
        "Course",
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.PROTECT,
    )
    grade = models.ForeignKey(
        "Grade",
        related_name="academics_educations",
        related_query_name="academic_education",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ["grade", "course"]

    def __str__(self):
        return f"{self.grade} em {self.course}"
