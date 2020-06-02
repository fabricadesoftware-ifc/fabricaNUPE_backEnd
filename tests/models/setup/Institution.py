from nupe.core.models import AcademicEducation, AcademicEducationCampus, Campus, Course, Grade
from tests.models.Course import COURSE_NAME, GRADE_NAME
from tests.models.setup.Location import create_location

CAMPUS_NAME = "Araquari"


def create_academic_education(*, course_name=COURSE_NAME, grade_name=GRADE_NAME):
    course = Course.objects.create(name=course_name)
    grade = Grade.objects.create(name=grade_name)

    return AcademicEducation.objects.create(course=course, grade=grade)


def create_academic_education_campus():
    location = create_location()
    campus = Campus.objects.create(name=CAMPUS_NAME, location=location)

    academic_education = create_academic_education()

    return AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
