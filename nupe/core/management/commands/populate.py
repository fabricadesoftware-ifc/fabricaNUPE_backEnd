import environ
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from model_bakery import baker

from nupe.account.models import Account
from nupe.core.models import (
    AcademicEducation,
    AcademicEducationCampus,
    Attendance,
    AttendanceReason,
    Campus,
    City,
    Function,
    Grade,
    Institution,
    Location,
    Person,
    Sector,
    State,
    Student,
)
from nupe.resources.datas.account.account import EMAIL, PASSWORD
from nupe.resources.datas.core.populate import (
    academic_educations,
    attendance_reasons,
    attendances,
    campi,
    cities,
    functions,
    institutions,
    persons,
    sectors,
    states,
    students,
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
            self.populate_persons()
            self.populate_students()
            self.populate_attendances()
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
            grade, _ = Grade.objects.get_or_create(name=academic_education_data.get("grade"))

            academic_education, _ = AcademicEducation.objects.get_or_create(
                name=academic_education_data.get("name"), grade=grade
            )
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

    def populate_persons(self):
        for person in persons:
            Person.objects.get_or_create(**person)

    def populate_students(self):
        for student in students:
            academic_education, campus_name = student.pop("academic_education_campus").split("-")

            try:
                person = Person.objects.get(cpf=student.pop("cpf"))

                academic_education_campus = AcademicEducationCampus.objects.get(
                    academic_education__name=academic_education.strip(), campus__name=campus_name.strip()
                )

                Student.objects.get_or_create(
                    **student, person=person, academic_education_campus=academic_education_campus
                )

            except Person.DoesNotExist or AcademicEducationCampus.DoesNotExist:
                message = """Pessoa ou Formação Acadêmica do Campus não encontrado.
                Por favor, informe na lista para população."""

                raise ValueError(message)

    def populate_attendances(self):
        for attendance in attendances:
            try:
                attendance_reason = AttendanceReason.objects.get(name=attendance.pop("attendance_reason"))

                student = Student.objects.get(registration=attendance.pop("registration"))

                Attendance.objects.get_or_create(**attendance, attendance_reason=attendance_reason, student=student)

            except AttendanceReason.DoesNotExist or Student.DoesNotExist:
                message = (
                    "Motivo de Atendimento ou Estudante não encontrado. Por favor, informe na lista para população."
                )

                raise ValueError(message)

    def populate_superuser(self):
        """
        Popula o banco de dados com um usuário comum padrão. Consulte o usuário e senha na documentação da API
        """
        email = env("DJANGO_SUPERUSER_EMAIL", default=EMAIL)
        password = env("DJANGO_SUPERUSER_PASSWORD", default=PASSWORD)

        try:
            function, _ = Function.objects.get_or_create(name="Psicóloga(o)")
            sector, _ = Sector.objects.get_or_create(name="Coordenadoria-Geral de Assistência Estudantil")

            Account.objects.create_superuser(
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
            Institution.objects.get_or_create(**institution)

    def __state_register(self):
        for state in states:
            State.objects.get_or_create(**state)

    def __city_register(self):
        for city_data in cities:
            city, _ = City.objects.get_or_create(name=city_data.get("name"))

            try:
                state = State.objects.get(initials=city_data.get("state_initials"))
                state.cities.add(city)

            except State.DoesNotExist:
                message = "Estado não cadastrado. Por favor, informe-o na lista para população."

                raise ValueError(message)
