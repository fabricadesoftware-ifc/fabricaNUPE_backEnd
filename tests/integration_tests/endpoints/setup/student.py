from datetime import date

from nupe.core.models import Student
from resources.const.datas.student import INGRESS_DATE, REGISTRATION
from tests.integration_tests.endpoints.setup.person import create_person
from tests.unit_tests.models.setup.institution import create_academic_education_campus


def create_student(*, registration: str = REGISTRATION, ingress_date: date = INGRESS_DATE, **kwargs) -> Student:
    person = create_person(**kwargs)
    academic_education_campus = create_academic_education_campus()

    return Student.objects.create(
        registration=registration,
        person=person,
        academic_education_campus=academic_education_campus,
        ingress_date=ingress_date,
    )
