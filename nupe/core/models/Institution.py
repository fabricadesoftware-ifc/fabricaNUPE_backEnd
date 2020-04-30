from django.db import models

from nupe.core.models import AcademicEducation, Location

INSTITUTION_MAX_LENGTH = 50
CAMPUS_MAX_LENGTH = 50


class Institution(models.Model):
    name = models.CharField(max_length=INSTITUTION_MAX_LENGTH, unique=True, verbose_name="nome")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name is not None:
            self.name = self.name.strip()
        return super().clean_fields(exclude=exclude)


class Campus(models.Model):
    name = models.CharField(max_length=CAMPUS_MAX_LENGTH, unique=True, verbose_name="nome")
    location = models.ForeignKey(Location, related_name="campus", on_delete=models.PROTECT, verbose_name="localização")
    institutions = models.ManyToManyField(
        Institution, related_name="campus", through="InstitutionCampus", verbose_name="instituições"
    )
    academic_education = models.ManyToManyField(
        AcademicEducation, related_name="campus", through="AcademicEducationCampus", verbose_name="formação acadêmica"
    )

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campus"

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.name is not None:
            self.name = self.name.strip()
        return super().clean_fields(exclude=exclude)


class InstitutionCampus(models.Model):
    institution = models.ForeignKey(
        Institution, related_name="institution_campus", on_delete=models.PROTECT, verbose_name="instituição",
    )
    campus = models.ForeignKey(Campus, related_name="institution_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["institution", "campus"]
        verbose_name = "Instituição - Campus"
        verbose_name_plural = "Instituições do Campus"

    def __str__(self):
        return "{} - {}".format(self.institution, self.campus)


class AcademicEducationCampus(models.Model):
    academic_education = models.ForeignKey(
        AcademicEducation, related_name="course_campus", on_delete=models.PROTECT, verbose_name="formação acadêmica",
    )
    campus = models.ForeignKey(Campus, related_name="course_campus", on_delete=models.PROTECT)

    class Meta:
        unique_together = ["campus", "academic_education"]
        verbose_name = "Formação Acadêmica - Campus"
        verbose_name_plural = "Formações Acadêmica do Campus"

    def __str__(self):
        return "Formação {} ofertada pelo Campus {}".format(self.academic_education, self.campus)
