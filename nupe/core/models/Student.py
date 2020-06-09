from django.core.exceptions import ValidationError
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.Regex import ONLY_NUMBERS
from resources.const.messages.Responsible import MYSELF_RESPONSIBLE_MESSAGE, UNDER_AGE_RESPONSIBLE_MESSAGE

STUDENT_REGISTRATION_MAX_LENGTH = 35
RESPONSIBLE_MIN_AGE = 18


class Student(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    _academic_education_campus_deleted_id = models.IntegerField(default=None, null=True, blank=True)

    registration = models.CharField(max_length=STUDENT_REGISTRATION_MAX_LENGTH, validators=[ONLY_NUMBERS], unique=True)
    person = models.ForeignKey("Person", related_name="student_registrations", on_delete=models.CASCADE)
    academic_education_campus = models.ForeignKey(
        "AcademicEducationCampus", related_name="students", null=True, on_delete=models.SET_NULL
    )
    responsibles_persons = models.ManyToManyField(
        "Person", related_name="dependents_students", related_query_name="student", through="Responsible"
    )
    graduated = models.BooleanField(default=False, null=True, blank=True)
    ingress_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["person", "academic_education_campus"]

    @property
    def age(self):
        return self.person.age

    @property
    def academic_education(self):
        return str(self.academic_education_campus.academic_education)

    def __str__(self):
        return f"{self.person} - {self.registration}"


class Responsible(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    student = models.ForeignKey(
        "Student", related_name="responsibles", related_query_name="responsible", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "Person", related_name="dependents", related_query_name="dependent", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["student", "person"]

    def clean(self):
        # o responsável não pode ser o próprio estudante se o estudante for menor de idade
        if self.student.age < RESPONSIBLE_MIN_AGE and self.student.person.id is self.person.id:
            raise ValidationError({"person": MYSELF_RESPONSIBLE_MESSAGE})

        # o responsável não pode ser menor de idade
        elif self.person.age < RESPONSIBLE_MIN_AGE:
            raise ValidationError({"person": UNDER_AGE_RESPONSIBLE_MESSAGE})

    def __str__(self):
        return f"{self.person} responsável de {self.student.person}"
