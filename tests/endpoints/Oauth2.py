import json

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from tests.endpoints.setup import (
    create_application,
    create_basic_authorization,
    create_user_with_permissions,
    get_access_token,
)

CLIENT_ID = "teste"
CLIENT_SECRET = "teste"
USERNAME = "teste123"
PASSWORD = USERNAME


class Oauth2APITestCase(APITestCase):
    def setUp(self):
        create_application(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        # permissão de list atribuída para testar o revoke token
        create_user_with_permissions(username=USERNAME, permissions=["core.view_person"])

    def test_get_access_token(self):
        client = self.client  # instância de APIClient

        basic_authorization = create_basic_authorization(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        # retorna um objeto HttpResponse
        response = get_access_token(
            authorization=basic_authorization, client=client, username=USERNAME, password=PASSWORD
        )

        # HttpResponse.content retorna um bytestring, por isso, é necessário obter a string e converter em dict
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotEqual(response_data.get("access_token"), None)  # deve retornar um token de acesso

    def test_refresh_token(self):
        client = self.client

        basic_authorization = create_basic_authorization(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        # necessário para obter o refresh token para enviar na requisição
        response = get_access_token(
            authorization=basic_authorization, client=client, username=USERNAME, password=PASSWORD
        )
        response_data = json.loads(response.content.decode())

        data = {
            "username": USERNAME,
            "password": PASSWORD,
            "grant_type": "refresh_token",
            "refresh_token": response_data.get("refresh_token"),
        }
        url = reverse("oauth2_provider:token")

        response = client.post(path=url, data=data, format="multipart")
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotEqual(response_data.get("access_token"), None)  # deve retornar um novo token de acesso

    def test_revoke_token(self):
        client = self.client

        basic_authorization = create_basic_authorization(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        response = get_access_token(
            authorization=basic_authorization, client=client, username=USERNAME, password=PASSWORD
        )
        response_data = json.loads(response.content.decode())

        # autorização necessária para consumir os endpoints
        access_token = response_data.get("access_token")
        bearer_authorization = f"Bearer {access_token}"

        client.credentials(HTTP_AUTHORIZATION=bearer_authorization)
        url = reverse("person-list")
        response = client.get(path=url)

        # com um token válido e com permissão, deve permitir acesso
        self.assertEqual(response.status_code, HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION=basic_authorization)
        url = reverse("oauth2_provider:revoke-token")
        data = {"token": access_token}

        # o token deve ser revogado, ou seja, não será mais válido
        response = client.post(path=url, data=data, format="multipart")

        self.assertEqual(response.status_code, HTTP_200_OK)  # o revoke deve ser aplicado

        client.credentials(HTTP_AUTHORIZATION=bearer_authorization)
        url = reverse("person-list")
        response = client.get(path=url)

        # com o token agora inválido, não deverá mais ter acesso
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
