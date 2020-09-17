from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import Campus, Institution
from nupe.resources.const.datas.institution import CAMPUS_NAME, INSTITUTION_NAME
from nupe.tests.integration_tests.endpoints.setup.user import create_user_with_permissions_and_do_authentication


class InstitutionAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Institution)  # cria uma instituição no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_institution"])
        url = reverse("institution-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Institution.objects.count())

    def test_retrieve_with_permission(self):
        institution = baker.make(Institution)  # cria uma instituição no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_institution"])
        url = reverse("institution-detail", args=[institution.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da instituição fornecida
        self.assertEqual(response.data.get("name"), institution.name)

    def test_create_with_permission(self):
        # instituição com informações válidas para conseguir criar
        institution = {"name": INSTITUTION_NAME}

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_institution"])
        url = reverse("institution-list")

        response = client.post(path=url, data=institution)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), institution.get("name"))
        self.assertEqual(Institution.objects.count(), 1)  # deve ser criado no banco de dados

    def test_partial_update_with_permission(self):
        institution = baker.make(Institution)  # cria uma instituição no banco para poder atualizar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_institution"])
        url = reverse("institution-detail", args=[institution.id])

        new_name = "name updated"
        institution_update = {
            "name": new_name,
        }

        response = client.patch(path=url, data=institution_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Institution.objects.get(pk=institution.id).name, new_name)

    def test_destroy_with_permission(self):
        institution = baker.make(Institution)  # cria uma instituição no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_institution"])
        url = reverse("institution-detail", args=[institution.id])

        response = client.delete(path=url)

        # o dado não deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Institution.objects.count(), 1)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("institution-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("institution-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_institution"])

        url = reverse("institution-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_institution"])

        url = reverse("institution-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_institution"])

        url = reverse("institution-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class CampusAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Campus)  # cria um campus no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_campus"])
        url = reverse("campus-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Campus.objects.count())

    def test_retrieve_with_permission(self):
        campus = baker.make(Campus)  # cria um campus no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_campus"])
        url = reverse("campus-detail", args=[campus.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do campus fornecido
        self.assertEqual(response.data.get("name"), campus.name)

    def test_create_with_permission(self):
        location = baker.make("core.Location")

        # campus com informações válidas para conseguir criar
        campus = {
            "name": CAMPUS_NAME,
            "location": location.id,
        }

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_campus"])
        url = reverse("campus-list")

        response = client.post(path=url, data=campus)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), campus.get("name"))
        self.assertEqual(Campus.objects.count(), 1)  # deve ser criado no banco de dados

    def test_partial_update_with_permission(self):
        campus = baker.make(Campus)  # cria um campus no banco para poder atualizar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_campus"])
        url = reverse("campus-detail", args=[campus.id])

        new_name = "name updated"
        campus_update = {
            "name": new_name,
        }

        response = client.patch(path=url, data=campus_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Campus.objects.get(pk=campus.id).name, new_name)

    def test_destroy_with_permission(self):
        campus = baker.make(Campus)  # cria um campus no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_campus"])
        url = reverse("campus-detail", args=[campus.id])

        response = client.delete(path=url)

        # o dado não deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Campus.objects.count(), 1)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("campus-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("campus-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_campus"])

        url = reverse("campus-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_campus"])

        url = reverse("campus-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_campus"])

        url = reverse("campus-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
