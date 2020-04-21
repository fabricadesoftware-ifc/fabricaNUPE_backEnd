from django.contrib import admin

from nupe.core.models import City, Location, State

location = [City, State, Location]

admin.site.register(location)
