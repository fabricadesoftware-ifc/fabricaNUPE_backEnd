from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class UserAPITestCase(APITestCase):
    def test_current_user(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("user-current")

        response = client.get(path=url)
        data = response.data.get("user")

        self.assertEqual(response.status_code, HTTP_200_OK)

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("first_name"))
        self.assertIsNotNone(data.get("last_name"))

        # campos que não devem ser retornados
