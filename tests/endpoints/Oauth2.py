import json

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from resources.const.datas.User import PASSWORD, USERNAME
from tests.endpoints.setup.Token import get_access_token, revoke_access_token
from tests.endpoints.setup.User import create_user_with_permissions


class Oauth2APITestCase(APITestCase):
    def setUp(self):
        # permissão de list atribuída para testar o revoke token
        create_user_with_permissions(username=USERNAME, permissions=["core.view_person"])

    def test_get_access_token(self):
        # retorna um objeto HttpResponse
        response, client = get_access_token(username=USERNAME, password=PASSWORD)

        # HttpResponse.content retorna um bytestring, por isso, é necessário obter a string e converter em dict
        response_data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotEqual(response_data.get("access_token"), None)  # deve retornar um token de acesso

    def test_refresh_token(self):
        # necessário para obter o refresh token para enviar na requisição
        response, client = get_access_token(username=USERNAME, password=PASSWORD)
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
        response, client = get_access_token(username=USERNAME, password=PASSWORD)
        response_data = json.loads(response.content.decode())

        # header necessário para consumir os endpoints
        access_token = response_data.get("access_token")
        bearer_authorization = f"Bearer {access_token}"

        client.credentials(HTTP_AUTHORIZATION=bearer_authorization)
        url = reverse("person-list")
        response = client.get(path=url)

        # com um token válido e com permissão, deve permitir acesso
        self.assertEqual(response.status_code, HTTP_200_OK)

        # o token deve ser revogado, ou seja, não será mais válido
        response = revoke_access_token(access_token=access_token)

        self.assertEqual(response.status_code, HTTP_200_OK)  # o revoke deve ser aplicado

        # com o token agora inválido, não deverá mais ter acesso
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
