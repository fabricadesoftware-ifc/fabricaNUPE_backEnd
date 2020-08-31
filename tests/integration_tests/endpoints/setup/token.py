from base64 import b64encode

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APIClient

from tests.integration_tests.endpoints.setup.application import create_application


def get_access_token(*, username: str, password: str) -> (HttpResponse, APIClient):
    """
    Configura o token básico no header e obtem o token de acesso

    Args:
        username (str): username para autenticação
        password (str): password para autenticação

    Returns:
        HttpResponse: response com os dados do token de acesso
        APIClient: client configurado com o token básico no header
    """
    client = config_request_header_basic_authorization()

    data = {"username": username, "password": password, "grant_type": "password"}
    url = reverse("oauth2_provider:token")

    return client.post(path=url, data=data), client


def revoke_access_token(*, access_token: str) -> HttpResponse:
    """
    Configura o token básico no header e revoga o token de acesso

    Args:
        access_token (str): token de acesso a ser revogado

    Returns:
        HttpResponse: response com status e content
    """
    client = config_request_header_basic_authorization()

    data = {"token": access_token}
    url = reverse("oauth2_provider:revoke-token")

    response = client.post(path=url, data=data)

    return response


def create_basic_authorization(*, client_id: str, client_secret: str) -> str:
    """
    Cria o token básico que é baseado na string 'foo:bar' em base64, onde foo e bar
    são o client_id e client_secret respectivamente

    Args:
        client_id (str): client_id da aplicação
        client_secret (str): client_secret da aplicação

    Returns:
        str: retorna o token básico em base64
    """
    string = f"{client_id}:{client_secret}"

    token = b64encode(string.encode())

    return f"Basic {token.decode()}"


def config_request_header_basic_authorization() -> APIClient:
    """
    Cria uma aplicação e o token básico para atribuir ao parâmetro 'Authorization' no Header

    Returns:
        APIClient: retorna um objeto com o Header Authorization configurado
    """
    client = APIClient()

    application = create_application()

    basic_authorization = create_basic_authorization(
        client_id=application.client_id, client_secret=application.client_secret
    )

    client.credentials(HTTP_AUTHORIZATION=basic_authorization)

    return client
