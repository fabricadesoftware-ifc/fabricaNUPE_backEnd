import os

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from model_bakery import baker

from nupe.account.models import Account
from nupe.core.models import (
    AcademicEducation,
    AcademicEducationInstitutionCampus,
    Campus,
    City,
    Course,
    Grade,
    Institution,
    InstitutionCampus,
    Location,
    State,
)
from nupe.resources.datas.account.account import EMAIL, PASSWORD
from nupe.resources.datas.core.populate import academic_educations, campi, cities, institutions, states


class Command(BaseCommand):
    """
    Popula o banco de dados com informações mínimas.

    Raises:
        CommandError: Algo de errado não está certo
    """

    help = "Popula o banco de dados com informações mínimas"

    def handle(self, *args, **options):
        try:
            self.populate_locations()
            self.populate_institutions()
            self.populate_academic_education()
            self.populate_superuser()

            self.stdout.write(self.style.SUCCESS("Tudo populado com sucesso! :D"))

        except CommandError:
            raise CommandError("Algo de errado não está certo")

    def populate_locations(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de municípios e estados
        """
        self.__state_register()
        self.__city_register()

    def populate_institutions(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de campi e instituições
        """
        self.__campus_register()
        self.__institution_register()

    def populate_academic_education(self):
        """
        Popula o banco de dados com base em uma lista pré-definida com nome, grau e qual campus oferece
        """
        for academic_education in academic_educations:
            course_object_model, _ = Course.objects.get_or_create(name=academic_education.get("course"))
            grade_object_model, _ = Grade.objects.get_or_create(name=academic_education.get("grade"))

            academic_education_object_model, _ = AcademicEducation.objects.get_or_create(
                course=course_object_model, grade=grade_object_model
            )
            try:
                (
                    academic_education_institution_campus_object_model,
                    _,
                ) = AcademicEducationInstitutionCampus.objects.get_or_create(
                    academic_education=academic_education_object_model,
                    institution_campus=InstitutionCampus.objects.get(
                        campus__name=academic_education.get("campus_name")
                    ),
                )
            except Campus.DoesNotExist:
                message = "Campus não encontrado. Por favor, informe na lista para população."

                raise ValueError(message)

    def populate_superuser(self):
        email = os.getenv(key="DJANGO_SUPERUSER_EMAIL", default=EMAIL)
        password = os.getenv(key="DJANGO_SUPERUSER_PASSWORD", default=PASSWORD)

        try:
            Account.objects.create_superuser(
                email=email, password=password, function=baker.make("core.Function"), sector=baker.make("core.Sector")
            )
        except IntegrityError:
            message = f"Super Usuário já criado!\nEmail: {email}\nSenha: {password}"

            raise ValueError(message)

    def __campus_register(self):
        for campus in campi:
            try:
                campus_object_model, _ = Campus.objects.get_or_create(
                    name=campus.get("name"), location=Location.objects.get(city__name=campus.get("location_city"))
                )

                institution_object_model, _ = Institution.objects.get_or_create(name=campus.get("institution_name"))
                campus_object_model.institutions.add(institution_object_model)

            except Location.DoesNotExist:
                message = "Localização não encontrada. Por favor, informe na lista para população."

                raise ValueError(message)

    def __institution_register(self):
        for institution in institutions:
            institution_object_model, _ = Institution.objects.get_or_create(name=institution.get("name"))

    def __state_register(self):
        for state in states:
            state_object_model, _ = State.objects.get_or_create(name=state.get("name"), initials=state.get("initials"))

    def __city_register(self):
        for city in cities:
            city_object_model, _ = City.objects.get_or_create(name=city.get("name"))

            try:
                state_object_model = State.objects.get(initials=city.get("state_initials"))
                state_object_model.cities.add(city_object_model)
            except State.DoesNotExist:
                message = "Estado não cadastrado. Por favor, informe-o na lista para população."

                raise ValueError(message)
