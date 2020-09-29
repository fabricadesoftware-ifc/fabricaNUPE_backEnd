from django.contrib import admin

from nupe.account.models import Account
from nupe.core.models import Person

admin.site.register([Account, Person])
