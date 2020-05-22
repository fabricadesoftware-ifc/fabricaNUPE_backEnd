import base64

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APIClient


def get_access_token(*, authorization: str, client: APIClient, username: str, password: str) -> HttpResponse:
    client.credentials(HTTP_AUTHORIZATION=authorization)
    data = {"username": username, "password": password, "grant_type": "password"}
    url = reverse("oauth2_provider:token")

    return client.post(path=url, data=data)


def create_basic_authorization(*, client_id: str, client_secret: str) -> str:
    # por padrão o token é criado em base64 a partir da string '<client_id>:<client_secret>'
    string = f"{client_id}:{client_secret}"
    token = base64.b64encode(string.encode())

    return f"Basic {token.decode()}"
