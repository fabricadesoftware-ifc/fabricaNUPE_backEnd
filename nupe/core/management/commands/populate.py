import json

import requests
from django.core.management.base import BaseCommand, CommandError

from nupe.core.models import City, State


class Command(BaseCommand):
    help = "Popula o banco de dados com informações mínimas. Isso pode demorar alguns minutos."

    def handle(self, *args, **options):
        try:
            self.populate_locations()
            self.stdout.write(self.style.SUCCESS("Tudo populado com sucesso! :D"))
        except:  # noqa
            raise CommandError("Alguma coisa deu errado.")

    def populate_locations(self):

        states_data = self.get_states()

        for state in states_data:
            state_object_model, created = self.save_state_on_database(state)

            counties_data = self.get_counties_from_state_id(state_id=state.get("id"))

            for county in counties_data:
                city_object_model, created = self.save_county_on_database(county)
                state_object_model.cities.add(city_object_model)

    def get_states(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

        return requests.get(url=url).json()

    def get_counties_from_state_id(self, state_id: int):
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_id}/municipios"

        return requests.get(url=url).json()

    def save_state_on_database(self, state: json):
        return State.objects.get_or_create(name=state.get("nome"), initials=state.get("sigla"))

    def save_county_on_database(self, county: json):
        return City.objects.get_or_create(name=county.get("nome"))
