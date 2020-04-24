from django.contrib import admin

from nupe.core.models import (
    City,
    State,
    Location,
    Course,
    Grade,
    AcademicEducation,
    Institution,
    Campus,
    InstitutionCampus,
    AcademicEducationCampus,
)

admin.site.register([City, State, Location])
admin.site.register([Course, Grade, AcademicEducation])
admin.site.register([Institution, Campus, InstitutionCampus, AcademicEducationCampus])
