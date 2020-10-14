import environ
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from model_bakery import baker

from nupe.account.models import Account
from nupe.core.models import (
    AcademicEducation,
    AcademicEducationCampus,
    AttendanceReason,
    Campus,
    City,
    Course,
    Function,
    Grade,
    Institution,
    Location,
    Sector,
    State,
)
from nupe.resources.datas.account.account import EMAIL, PASSWORD
from nupe.resources.datas.core.populate import (
    academic_educations,
    attendance_reasons,
    campi,
    cities,
    functions,
    institutions,
    sectors,
    states,
)

env = environ.Env()


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
            self.populate_sectors()
            self.populate_functions()
            self.populate_attendance_reasons()
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
        self.__institution_register()
        self.__campus_register()

    def populate_academic_education(self):
        """
        Popula o banco de dados com base em uma lista pré-definida com nome, grau e qual campus oferece
        """
        for academic_education_data in academic_educations:
            course, _ = Course.objects.get_or_create(name=academic_education_data.get("course"))
            grade, _ = Grade.objects.get_or_create(name=academic_education_data.get("grade"))

            academic_education, _ = AcademicEducation.objects.get_or_create(course=course, grade=grade)
            try:
                AcademicEducationCampus.objects.get_or_create(
                    academic_education=academic_education,
                    campus=Campus.objects.get(name=academic_education_data.get("campus_name")),
                )
            except Campus.DoesNotExist:
                message = "Campus não encontrado. Por favor, informe na lista para população."

                raise ValueError(message)

    def populate_sectors(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de setores
        """
        for sector in sectors:
            Sector.objects.get_or_create(**sector)

    def populate_functions(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de funções dos funcionários
        """
        for function in functions:
            Function.objects.get_or_create(**function)

    def populate_attendance_reasons(self):
        """
        Popula o banco de dados com base em uma lista pré-definida de motivos de atendimento
        """
        for attendance_reason_data in attendance_reasons:
            attendance_reason, _ = AttendanceReason.objects.get_or_create(name=attendance_reason_data.get("name"))

            for son_attendance_reason_data in attendance_reason_data.get("sons"):
                AttendanceReason.objects.get_or_create(
                    name=son_attendance_reason_data.get("name"), father_reason=attendance_reason
                )

    def populate_superuser(self):
        """
        Popula o banco de dados com um usuário comum padrão. Consulte o usuário e senha na documentação da API
        """
        email = env("DJANGO_SUPERUSER_EMAIL", default=EMAIL)
        password = env("DJANGO_SUPERUSER_PASSWORD", default=PASSWORD)

        try:
            function, _ = Function.objects.get_or_create(name="Psicóloga(o)")
            sector, _ = Sector.objects.get_or_create(name="Coordenadoria-Geral de Assistência Estudantil")

            Account.objects.create_user(
                email=email, password=password, person=baker.make("core.Person"), function=function, sector=sector,
            )
        except IntegrityError:
            message = f"Super Usuário já criado!\nEmail: {email}\nSenha: {password}\n"

            self.stdout.write(self.style.WARNING(message))

    def __campus_register(self):
        for campus in campi:
            try:
                city_name, state_initials = campus.pop("location").split("-")

                location = Location.objects.get(city__name=city_name.strip(), state__initials=state_initials.strip())
                institution = Institution.objects.get(name=campus.pop("institution"))

                campus = Campus.objects.get_or_create(**campus, location=location, institution=institution)

            except Location.DoesNotExist or Institution.DoesNotExist:
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
