from json import loads

from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.test import APITestCase

from nupe.resources.messages.custom_handler_404 import ENDPOINT_NOT_FOUND
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class CustomHandler404APITestCase(APITestCase):
    def test_endpoint_not_found(self):
        client = create_user_with_permissions_and_do_authentication()
        url = "not-found/"

        response = client.get(path=url)
        response_data = response.content.decode()

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

        # a mensagem informativa deve ser retornada
        self.assertEqual(loads(response_data).get("detail"), ENDPOINT_NOT_FOUND)
