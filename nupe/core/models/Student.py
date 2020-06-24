from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.Regex import ONLY_NUMBERS

STUDENT_REGISTRATION_MAX_LENGTH = 35
RESPONSIBLE_MIN_AGE = 18


class Student(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
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
    _safedelete_policy = SOFT_DELETE_CASCADE

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
