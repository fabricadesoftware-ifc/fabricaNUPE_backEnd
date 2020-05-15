from django.db import models

INSTITUTION_MAX_LENGTH = 50
CAMPUS_MAX_LENGTH = 50


class Institution(models.Model):
    name = models.CharField(max_length=INSTITUTION_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class Campus(models.Model):
    name = models.CharField(max_length=CAMPUS_MAX_LENGTH, unique=True)
    location = models.ForeignKey("Location", related_name="campus", on_delete=models.PROTECT)
    institutions = models.ManyToManyField("Institution", related_name="campus", through="InstitutionCampus")
    academic_education = models.ManyToManyField(
        "AcademicEducation", related_name="campus", through="AcademicEducationCampus",
    )

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name:
            self.name = self.name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.name = self.name.capitalize()


class InstitutionCampus(models.Model):
    institution = models.ForeignKey("Institution", related_name="institution_campus", on_delete=models.PROTECT)
    campus = models.ForeignKey("Campus", related_name="institution_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["institution", "campus"]

    def __str__(self):
        return f"{self.institution} - {self.campus}"


class AcademicEducationCampus(models.Model):
    academic_education = models.ForeignKey("AcademicEducation", related_name="course_campus", on_delete=models.PROTECT)
    campus = models.ForeignKey("Campus", related_name="course_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["campus", "academic_education"]

    def __str__(self):
        return f"Formação {self.academic_education} ofertada pelo Campus {self.campus}"
