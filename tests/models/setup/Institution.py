from nupe.core.models import AcademicEducation, AcademicEducationCampus, Campus, Course, Grade
from tests.models.setup import setup_create_location


def setup_create_academic_education(*, course_name, grade_name):
    course = Course.objects.create(name=course_name)
    grade = Grade.objects.create(name=grade_name)

    return AcademicEducation.objects.create(course=course, grade=grade)


def setup_create_academic_education_campus(*, course_name, grade_name, city_name, state_name, campus_name):
    academic_education = setup_create_academic_education(course_name=course_name, grade_name=grade_name)
    location = setup_create_location(city_name=city_name, state_name=state_name)
    campus = Campus.objects.create(name=campus_name, location=location)

    return AcademicEducationCampus.objects.create(academic_education=academic_education, campus=campus)
