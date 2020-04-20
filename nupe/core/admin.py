from django.contrib import admin

from nupe.core.models import Cidade, Estado, Localizacao

localizacao = [Localizacao, Cidade, Estado]

admin.site.register(localizacao)
