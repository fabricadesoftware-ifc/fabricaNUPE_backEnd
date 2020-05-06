from django.contrib import admin

from nupe.core.models import (
    AcademicEducation,
    AcademicEducationCampus,
    Campus,
    City,
    Course,
    Grade,
    Institution,
    InstitutionCampus,
    Location,
    Person,
    State,
)

admin.site.register([City, State, Location])
admin.site.register([Course, Grade, AcademicEducation])
admin.site.register([Institution, Campus, InstitutionCampus, AcademicEducationCampus])
admin.site.register(Person)
