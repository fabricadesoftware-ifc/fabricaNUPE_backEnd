from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from nupe.core.models import Student
from nupe.resources.datas.core.person import OLDER_BIRTHDAY_DATE
from nupe.resources.datas.core.student import INGRESS_DATE, REGISTRATION
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class StudentAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um estudante no banco para retornar no list
        baker.make(Student)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_student"])
        url = reverse("student-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Student.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("registration"))
        self.assertIsNotNone(data.get("full_name"))
        self.assertIsNotNone(data.get("ingress_date"))
        self.assertIsNotNone(data.get("graduated"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(data.get("person"))
        self.assertIsNone(data.get("academic_education_institution_campus"))
        self.assertIsNone(data.get("responsibles_persons"))
        self.assertIsNone(data.get("updated_at"))
        self.assertIsNone(data.get("responsibles"))
        self.assertIsNone(data.get("age"))
        self.assertIsNone(data.get("academic_education"))

    def test_retrieve_with_permission(self):
        # cria um estudante no banco para detalhar suas informações
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")
        student = baker.make(Student, academic_education_institution_campus=academic_education_institution_campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_student"])
        url = reverse("student-detail", args=[student.registration])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do estudante da matrícula fornecida
        self.assertEqual(response.data.get("registration"), student.registration)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("registration"))
        self.assertIsNotNone(response.data.get("personal_info"))
        self.assertIsNotNone(response.data.get("course"))
        self.assertIsNotNone(response.data.get("institution"))
        self.assertIsNotNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNotNone(response.data.get("responsibles"))
        self.assertIsNotNone(response.data.get("ingress_date"))
        self.assertIsNotNone(response.data.get("graduated"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_create_with_permission(self):
        under_age_person = baker.make("Person")
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student_data = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_institution_campus": academic_education_institution_campus.id,
            "responsibles": [older_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # o estudante deve ser criado no banco de dados
        student_object_model = Student.objects.all().first()
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student_object_model.registration, REGISTRATION)
        self.assertEqual(student_object_model.person, under_age_person)
        self.assertEqual(
            student_object_model.academic_education_institution_campus, academic_education_institution_campus
        )
        self.assertEqual(student_object_model.responsibles_persons.all().first(), older_person)
        self.assertEqual(student_object_model.ingress_date, INGRESS_DATE)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("registration"))
        self.assertIsNotNone(response.data.get("person"))
        self.assertIsNotNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNotNone(response.data.get("responsibles"))
        self.assertIsNotNone(response.data.get("ingress_date"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_partial_update_with_permission(self):
        # cria um estudante no banco para conseguir atualiza-lo
        student = baker.make(Student, person__birthday_date=OLDER_BIRTHDAY_DATE)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        # somente um campo e com informação válida para conseguir atualizar
        new_registration = REGISTRATION + "99"
        student_data = {"registration": new_registration}

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Student.objects.get(pk=student.id).registration, new_registration)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("registration"))
        self.assertIsNotNone(response.data.get("person"))
        self.assertIsNot(response.data.get("academic_education_institution_campus", False), False)
        self.assertIsNotNone(response.data.get("responsibles"))
        self.assertIsNotNone(response.data.get("ingress_date"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_destroy_with_permission(self):
        # cria um estudante no banco para conseguir mascara-lo
        student = baker.make(Student)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_student"])
        url = reverse("student-detail", args=[student.registration])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(Student.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Student.all_objects.count(), 1)

    def test_create_invalid_registration_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_registration = "teste"
        student = {
            "registration": invalid_registration,
            "person": older_person.id,
            "academic_education_institution_campus": academic_education_institution_campus.id,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("registration"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso o estudante seja menor de idade e não tenha sido informado um responsável
    def test_create_invalid_empty_responsible_with_permission(self):
        under_age_person = baker.make("Person")
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_institution_campus": academic_education_institution_campus.id,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso tenha sido informado um responsável que seja menor de idade
    def test_create_invalid_under_age_responsible_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        under_age_person = baker.make("Person")
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": older_person.id,
            "academic_education_institution_campus": academic_education_institution_campus.id,
            "responsibles": [under_age_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso o estudante seja menor de idade e tenha sido informado que ele é o próprio responsável
    def test_create_invalid_self_responsible_with_permission(self):
        under_age_person = baker.make("Person")
        academic_education_institution_campus = baker.make("AcademicEducationInstitutionCampus")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_institution_campus": academic_education_institution_campus.id,
            "responsibles": [under_age_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_partial_update_invalid_registration_with_permission(self):
        # cria um estudante no banco para conseguir atualiza-lo
        student = baker.make(Student)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_registration = "invalid_registration"
        student_data = {
            "registration": invalid_registration,
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("registration"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso o estudante seja menor de idade e não tenha sido informado um responsável
    def test_partial_update_invalid_empty_responsible_with_permission(self):
        student = baker.make(Student)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso tenha sido informado um responsável que seja menor de idade
    def test_partial_update_invalid_under_age_responsible_with_permission(self):
        student = baker.make(Student)
        under_age_person = baker.make("Person")

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [under_age_person.id],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    # caso o estudante seja menor de idade e tenha sido informado que ele é o próprio responsável
    def test_partial_update_invalid_self_responsible_with_permission(self):
        student = baker.make(Student)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [student.person.id],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("responsibles"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("_academic_education_institution_campus_deleted_id"))
        self.assertIsNone(response.data.get("registration"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("academic_education_institution_campus"))
        self.assertIsNone(response.data.get("responsibles_persons"))
        self.assertIsNone(response.data.get("graduated"))
        self.assertIsNone(response.data.get("ingress_date"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("age"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("student-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("student-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)