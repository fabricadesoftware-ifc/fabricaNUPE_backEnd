import base64

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APIClient

from resources.const.datas.oauth2 import CLIENT_ID, CLIENT_SECRET
from tests.endpoints.setup.application import get_or_create_application


def get_access_token(*, username: str, password: str) -> (HttpResponse, APIClient):
    client = config_request_header_basic_authorization()

    data = {"username": username, "password": password, "grant_type": "password"}
    url = reverse("oauth2_provider:token")

    response = client.post(path=url, data=data, format="multipart")

    return response, client


def revoke_access_token(*, access_token: str) -> HttpResponse:
    client = config_request_header_basic_authorization()

    data = {"token": access_token}
    url = reverse("oauth2_provider:revoke-token")

    response = client.post(path=url, data=data, format="multipart")

    return response


def create_basic_authorization(*, client_id: str, client_secret: str) -> str:
    # por padrão o token é criado em base64 a partir da string '<client_id>:<client_secret>'
    string = f"{client_id}:{client_secret}"
    token = base64.b64encode(string.encode())

    basic_authorization = f"Basic {token.decode()}"

    return basic_authorization


def config_request_header_basic_authorization() -> APIClient:
    client = APIClient()

    application = get_or_create_application(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    basic_authorization = create_basic_authorization(
        client_id=application.client_id, client_secret=application.client_secret
    )

    client.credentials(HTTP_AUTHORIZATION=basic_authorization)

    return client
