from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import City, Location, State
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class CityAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma cidade no banco para retornar no list
        baker.make(City)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_city"])
        url = reverse("city-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), City.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("states"))

    def test_retrieve_with_permission(self):
        # cria uma cidade no banco para detalhar suas informações
        city = baker.make(City)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_city"])
        url = reverse("city-detail", args=[city.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da cidade fornecida
        self.assertEqual(response.data.get("name"), str(city))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("states"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("city-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("city-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class StateAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um estado no banco para retornar no list
        baker.make(State)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_state"])
        url = reverse("state-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), State.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNotNone(data.get("initials"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("cities"))

    def test_retrieve_with_permission(self):
        # cria um estado no banco para detalhar suas informações
        state = baker.make(State)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_state"])
        url = reverse("state-detail", args=[state.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do estado fornecido
        self.assertEqual(response.data.get("name"), str(state))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("initials"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("cities"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("state-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("state-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class LocationAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma localização no banco para retornar no list
        baker.make(Location)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_location"])
        url = reverse("location-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Location.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("city"))
        self.assertIsNone(data.get("state"))
        self.assertIsNone(data.get("campus"))

    def test_retrieve_with_permission(self):
        # cria uma localização no banco para detalhar suas informações
        location = baker.make(Location)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_location"])
        url = reverse("location-detail", args=[location.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da localização fornecida
        self.assertEqual(response.data.get("name"), str(location))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("city"))
        self.assertIsNone(response.data.get("state"))
        self.assertIsNone(response.data.get("campus"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("location-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("location-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
