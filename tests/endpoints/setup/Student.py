from datetime import date

from nupe.core.models import Student
from tests.endpoints.setup import create_person
from tests.models.setup.Institution import create_academic_education_campus
from tests.models.Student import INGRESS_DATE, REGISTRATION


def create_student(*, registration: str = REGISTRATION, ingress_date: date = INGRESS_DATE) -> Student:
    person = create_person()
    academic_education_campus = create_academic_education_campus()

    return Student.objects.create(
        registration=registration,
        person=person,
        academic_education_campus=academic_education_campus,
        ingress_date=ingress_date,
    )
