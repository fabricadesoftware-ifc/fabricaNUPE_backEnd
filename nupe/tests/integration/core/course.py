from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import AcademicEducation, Grade
from nupe.resources.datas.core.course import ACADEMIC_EDUCATION_NAME, GRADE_NAME
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class GradeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um grau no banco para retornar no list
        baker.make(Grade)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Grade.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("academic_education"))

    def test_retrieve_with_permission(self):
        # cria um grau no banco para detalhar suas informações
        grade = baker.make(Grade)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do grau fornecido
        self.assertEqual(response.data.get("name"), grade.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_create_with_permission(self):
        # grau com informações válidas para conseguir criar
        grade_data = {"name": GRADE_NAME}

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_grade"])
        url = reverse("grade-list")

        response = client.post(path=url, data=grade_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        self.assertEqual(Grade.objects.count(), 1)
        self.assertEqual(Grade.objects.all().first().name, GRADE_NAME)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_partial_update_with_permission(self):
        # cria um grau no banco para conseguir atualizar suas informações
        grade = baker.make(Grade)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_grade"])
        url = reverse("grade-detail", args=[grade.id])

        new_name = "name updated"
        grade_update_data = {
            "name": new_name,
        }

        response = client.patch(path=url, data=grade_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Grade.objects.get(pk=grade.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_destroy_with_permission(self):
        # cria um grau no banco para conseguir excluir
        grade = baker.make(Grade)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(Grade.objects.count(), 0)

        # mas deve ser mantido no banco
        self.assertEqual(Grade.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class AcademicEducationAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma formação acadêmica no banco para retornar no list
        baker.make(AcademicEducation)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), AcademicEducation.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNotNone(data.get("grade"))
        self.assertIsNotNone(data.get("campi"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("academic_education_campus"))

    def test_retrieve_with_permission(self):
        # cria uma formação acadêmica no banco para detalhar suas informações
        academic_education = baker.make(AcademicEducation)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-detail", args=[academic_education.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da formação acadêmica fornecida
        self.assertEqual(response.data.get("name"), academic_education.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("grade"))
        self.assertIsNotNone(response.data.get("campi"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))

    def test_create_with_permission(self):
        # formação acadêmica com informações válidas para conseguir criar
        grade = baker.make("core.Grade")
        campus = baker.make("core.Campus")

        academic_education_data = {
            "name": ACADEMIC_EDUCATION_NAME,
            "grade": grade.id,
            "campi": [campus.id],
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_academiceducation"])
        url = reverse("academic_education-list")

        response = client.post(path=url, data=academic_education_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        self.assertEqual(AcademicEducation.objects.count(), 1)
        self.assertEqual(AcademicEducation.objects.all().first().name, ACADEMIC_EDUCATION_NAME)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("grade"))
        self.assertIsNotNone(response.data.get("campi"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))

    def test_partial_update_with_permission(self):
        # cria uma formação acadêmica no banco para conseguir atualizar suas informações
        academic_education = baker.make(AcademicEducation)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_academiceducation"])
        url = reverse("academic_education-detail", args=[academic_education.id])

        new_name = "name updated"
        academic_education_data = {
            "name": new_name,
        }

        response = client.patch(path=url, data=academic_education_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(AcademicEducation.objects.get(pk=academic_education.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("grade"))
        self.assertIsNotNone(response.data.get("campi"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))

    def test_destroy_with_permission(self):
        # cria uma formação acadêmica no banco para conseguir excluir
        academic_education = baker.make(AcademicEducation)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_academiceducation"])
        url = reverse("academic_education-detail", args=[academic_education.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(AcademicEducation.objects.count(), 0)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("academic_education-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("academic_education-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("academic_education-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("academic_education-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("academic_education-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
