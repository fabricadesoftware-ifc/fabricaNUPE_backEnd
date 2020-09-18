from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import Student
from nupe.resources.datas.core.person import OLDER_BIRTHDAY_DATE
from nupe.resources.datas.core.student import INGRESS_DATE, REGISTRATION
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class StudentAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um estudante no banco para retornar no list
        baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_student"])
        url = reverse("student-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os estudantes do banco de dados
        self.assertEqual(response.data.get("count"), Student.objects.count())

    def test_retrieve_with_permission(self):
        # cria um estudante no banco para detalhar suas informações
        academic_education_campus = baker.make("AcademicEducationCampus")
        student = baker.make(Student, academic_education_campus=academic_education_campus)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_student"])
        url = reverse("student-detail", args=[student.registration])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do estudante do registration fornecido
        self.assertEqual(response.data.get("registration"), student.registration)

    def test_create_with_permission(self):
        under_age_person = baker.make("Person")
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student_data = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [older_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("person"), under_age_person.id)
        self.assertEqual(Student.objects.count(), 1)  # o estudante deve ser criado no banco de dados

    def test_partial_update_with_permission(self):
        # cria um estudante no banco para poder atualiza-lo
        student = baker.make(Student, person__birthday_date=OLDER_BIRTHDAY_DATE)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        # somente um campo e com informação válida para conseguir atualizar
        new_registration = REGISTRATION + "99"
        student_data = {"registration": new_registration}

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Student.objects.get(pk=student.id).registration, new_registration)

    def test_destroy_with_permission(self):
        # cria um estudante no banco para poder mascara-lo
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_student"])
        url = reverse("student-detail", args=[student.registration])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)  # deve ser mascarado
        self.assertEqual(Student.all_objects.count(), 1)  # mas deve ser mantido no banco de dados

    def test_create_invalid_registration_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_registration = "teste"  # registration deve conter somente números
        student = {
            "registration": invalid_registration,
            "person": older_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("registration"))

    def test_create_invalid_person_not_exist_with_permission(self):
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_pk_person = 99  # não existe no banco de teste porque inicia-se vazio
        student = {
            "registration": REGISTRATION,
            "person": invalid_pk_person,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("person"))

    def test_create_invalid_responsible_not_exist_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_pk_responsible = 99
        student = {
            "registration": REGISTRATION,
            "person": older_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [invalid_pk_responsible],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso o estudante seja menor de idade e não tenha sido informado um responsável
    def test_create_invalid_empty_responsible_with_permission(self):
        under_age_person = baker.make("Person")
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso tenha sido informado um responsável que seja menor de idade
    def test_create_invalid_under_age_responsible_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        under_age_person = baker.make("Person")
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": older_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [under_age_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso o estudante seja menor de idade e tenha sido informado que ele é o próprio responsável
    def test_create_invalid_self_responsible_with_permission(self):
        under_age_person = baker.make("Person")
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        student = {
            "registration": REGISTRATION,
            "person": under_age_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [under_age_person.id],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    def test_create_invalid_academic_education_campus_not_exist_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_pk_academic_education_campus = 99
        student = {
            "registration": REGISTRATION,
            "person": older_person.id,
            "academic_education_campus": invalid_pk_academic_education_campus,
            "responsibles": [],
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("academic_education_campus"))

    def test_create_invalid_ingress_date_with_permission(self):
        older_person = baker.make("Person", birthday_date=OLDER_BIRTHDAY_DATE)
        academic_education_campus = baker.make("AcademicEducationCampus")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_student"])
        url = reverse("student-list")

        invalid_ingress_date = "14/02/1999"  # formato válido: yyyy-MM-dd
        student = {
            "registration": REGISTRATION,
            "person": older_person.id,
            "academic_education_campus": academic_education_campus.id,
            "responsibles": [],
            "ingress_date": invalid_ingress_date,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("ingress_date"))

    def test_partial_update_invalid_registration_with_permission(self):
        # cria um estudante no banco para poder atualiza-lo
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_registration = "invalid_registration"
        student_data = {
            "registration": invalid_registration,
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("registration"))

    def test_partial_update_invalid_person_not_exist_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_pk_person = 99
        student_data = {
            "person": invalid_pk_person,
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("person"))

    def test_partial_update_invalid_responsible_not_exist_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_pk_responsible = 99
        student_data = {
            "responsibles": [invalid_pk_responsible],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso o estudante seja menor de idade e não tenha sido informado um responsável
    def test_partial_update_invalid_empty_responsible_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso tenha sido informado um responsável que seja menor de idade
    def test_partial_update_invalid_under_age_responsible_with_permission(self):
        student = baker.make(Student)
        under_age_person = baker.make("Person")

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [under_age_person.id],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    # caso o estudante seja menor de idade e tenha sido informado que ele é o próprio responsável
    def test_partial_update_invalid_self_responsible_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        student_data = {
            "responsibles": [student.person.id],
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("responsibles"))

    def test_partial_update_invalid_academic_education_campus_not_exist_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_pk_academic_education_campus = 99
        student_data = {
            "academic_education_campus": invalid_pk_academic_education_campus,
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("academic_education_campus"))

    def test_partial_update_invalid_ingress_date_with_permission(self):
        student = baker.make(Student)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])
        url = reverse("student-detail", args=[student.registration])

        invalid_ingress_date = "14/02/1999"
        student_data = {
            "ingress_date": invalid_ingress_date,
        }

        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("ingress_date"))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("student-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("student-list")
        response = client.post(path=url, data={})

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("student-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_student"])

        url = reverse("student-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_student"])

        url = reverse("student-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_student"])

        url = reverse("student-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
