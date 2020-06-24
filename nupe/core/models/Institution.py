from django.db import models
from safedelete.models import NO_DELETE, SOFT_DELETE_CASCADE, SafeDeleteModel

INSTITUTION_MAX_LENGTH = 50
CAMPUS_MAX_LENGTH = 50


class Institution(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    name = models.CharField(max_length=INSTITUTION_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Campus(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    name = models.CharField(max_length=CAMPUS_MAX_LENGTH, unique=True)
    location = models.ForeignKey("Location", related_name="campus", on_delete=models.PROTECT)
    institutions = models.ManyToManyField("Institution", related_name="campus", through="InstitutionCampus")
    academic_education = models.ManyToManyField(
        "AcademicEducation", related_name="campus", through="AcademicEducationCampus",
    )

    def __str__(self):
        return self.name


class InstitutionCampus(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    institution = models.ForeignKey("Institution", related_name="institution_campus", on_delete=models.PROTECT)
    campus = models.ForeignKey("Campus", related_name="institution_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["institution", "campus"]

    def __str__(self):
        return f"{self.institution} - {self.campus}"


class AcademicEducationCampus(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    academic_education = models.ForeignKey("AcademicEducation", related_name="course_campus", on_delete=models.CASCADE)
    campus = models.ForeignKey("Campus", related_name="course_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["campus", "academic_education"]

    def __str__(self):
        return f"{self.academic_education} - {self.campus}"
