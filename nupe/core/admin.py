from django.contrib import admin

from nupe.core.models import City, State, Location
from nupe.core.models import Course, Grade, AcademicEducation

admin.site.register([City, State, Location])
admin.site.register([Course, Grade, AcademicEducation])
