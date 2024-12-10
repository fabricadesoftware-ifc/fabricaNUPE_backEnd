from django.contrib import admin

from nupe.core.models.attendance import AccountAttendance, Attendance
from nupe.core.models.course import AcademicEducation, AcademicEducationCampus, Grade
from nupe.core.models.institution import Campus, Institution
from nupe.core.models.job import Function, Sector
from nupe.core.models.location import City, Location, State
from nupe.core.models.person import Person
from nupe.core.models.reason import AttendanceReason
from nupe.core.models.student import Responsible, Student
from nupe.core.models.team import Team

admin.site.register(Function)
admin.site.register(Sector)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Location)
admin.site.register(Campus)
admin.site.register(Institution)
admin.site.register(Person)
admin.site.register(Responsible)
admin.site.register(Student)
admin.site.register(Team)