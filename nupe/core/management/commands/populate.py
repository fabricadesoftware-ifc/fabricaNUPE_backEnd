import json

import requests
from django.core.management.base import BaseCommand, CommandError

from nupe.core.management.commands._academic_education_list import academic_educations
from nupe.core.models import Campus, City, Course, Grade, Institution, Location, State


class Command(BaseCommand):
    """
    Popula o banco de dados com informações mínimas. Isso pode demorar alguns minutos.

    Raises:
        CommandError: Algo de errado não está certo
    """

    help = "Popula o banco de dados com informações mínimas. Isso pode demorar alguns minutos."

    INSTITUTION_BASENAME = "Instituto Federal Catarinense"
    CAMPUS_BASENAME = "Araquari"

    def handle(self, *args, **options):
        try:
            self.populate_locations()
            self.populate_academic_education()
            self.populate_institutions()
            self.stdout.write(self.style.SUCCESS("Tudo populado com sucesso! :D"))
        except CommandError:  # noqa
            raise CommandError("Algo de errado não está certo")

    def populate_locations(self):
        """
        Utiliza a API do IBGE para buscar os estados e cidades do Brasil e popular o banco de dados
        """
        if self.__already_was_populated():
            return

        states_data = self.__get_states()

        for state in states_data:
            state_object_model, state_created = self.__save_state_on_database(state)

            counties_data = self.__get_counties_from_state_id(state_id=state.get("id"))

            for county in counties_data:
                city_object_model, city_created = self.__save_county_on_database(county)

                if city_created:
                    state_object_model.cities.add(city_object_model)

    def populate_academic_education(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de cursos oferecidos pelo
        Instituto Federal Catarinense - Campus Araquari
        """
        for academic_education in academic_educations:
            course_object_model, course_created = Course.objects.get_or_create(name=academic_education.get("course"))
            grade_object_model, grade_created = Grade.objects.get_or_create(name=academic_education.get("grade"))

            if course_created:
                grade_object_model.courses.add(course_object_model)

    def populate_institutions(self):
        """
        Cadastra o Instituto Federal Catarinense e o Campus Araquari no banco de dados
        """
        institution_object_model, institution_created = Institution.objects.get_or_create(
            name=self.INSTITUTION_BASENAME
        )

        location_object_model = Location.objects.get(city__name=self.CAMPUS_BASENAME)
        campus_object_model, campus_created = Campus.objects.get_or_create(
            name=self.CAMPUS_BASENAME, location=location_object_model
        )

        if institution_created:
            campus_object_model.institutions.add(institution_object_model)

    def __get_states(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

        return requests.get(url=url).json()

    def __get_counties_from_state_id(self, state_id: int):
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_id}/municipios"

        return requests.get(url=url).json()

    def __save_state_on_database(self, state: json):
        return State.objects.get_or_create(name=state.get("nome"), initials=state.get("sigla"))

    def __save_county_on_database(self, county: json):
        return City.objects.get_or_create(name=county.get("nome"))

    def __already_was_populated(self):
        return Location.objects.count() == 5570  # 5570 é a quantidade de municípios no Brasil
