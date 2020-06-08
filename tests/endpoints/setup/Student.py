from datetime import date

from nupe.core.models import Student
from resources.const.datas.Student import INGRESS_DATE, REGISTRATION
from tests.endpoints.setup.Person import create_person
from tests.models.setup.Institution import create_academic_education_campus


def create_student(*, registration: str = REGISTRATION, ingress_date: date = INGRESS_DATE) -> Student:
    person = create_person()
    academic_education_campus = create_academic_education_campus()

    return Student.objects.create(
        registration=registration,
        person=person,
        academic_education_campus=academic_education_campus,
        ingress_date=ingress_date,
    )
