from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.test import APITestCase

from nupe.core.models import City, Location, State
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class LocationAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Location)  # cria uma localização no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_location"])
        url = reverse("location-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Location.objects.count())

    def test_retrieve_with_permission(self):
        location = baker.make(Location)  # cria uma localização no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_location"])
        url = reverse("location-detail", args=[location.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da localização fornecida
        self.assertEqual(response.data.get("name"), str(location))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("location-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("location-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_location"])

        url = reverse("location-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe


class CityAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(City)  # cria uma cidade no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_city"])
        url = reverse("city-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), City.objects.count())

    def test_retrieve_with_permission(self):
        city = baker.make(City)  # cria uma cidade no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_city"])
        url = reverse("city-detail", args=[city.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da cidade fornecida
        self.assertEqual(response.data.get("name"), str(city))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("city-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("city-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_city"])

        url = reverse("city-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe


class StateAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(State)  # cria um estado no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_state"])
        url = reverse("state-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), State.objects.count())

    def test_retrieve_with_permission(self):
        state = baker.make(State)  # cria um estado no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_state"])
        url = reverse("state-detail", args=[state.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do estado fornecido
        self.assertEqual(response.data.get("name"), str(state))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("state-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("state-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_state"])

        url = reverse("state-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe
