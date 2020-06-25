from nupe.core.models import AcademicEducation, AcademicEducationCampus, Campus, Course, Grade
from resources.const.datas.course import COURSE_NAME, GRADE_NAME
from resources.const.datas.institution import CAMPUS_NAME
from tests.models.setup.location import create_location


def create_academic_education(*, course_name: str = COURSE_NAME, grade_name: str = GRADE_NAME):
    course, created = Course.objects.get_or_create(name=course_name)
    grade, created = Grade.objects.get_or_create(name=grade_name)

    academic_education, created = AcademicEducation.objects.get_or_create(course=course, grade=grade)

    return academic_education


def create_academic_education_campus():
    location = create_location()
    campus, created = Campus.objects.get_or_create(name=CAMPUS_NAME, location=location)

    academic_education = create_academic_education()

    academic_education_campus, created = AcademicEducationCampus.objects.get_or_create(
        academic_education=academic_education, campus=campus
    )

    return academic_education_campus
