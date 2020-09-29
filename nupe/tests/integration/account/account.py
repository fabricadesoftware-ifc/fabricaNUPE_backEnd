from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class AccountAPITestCase(APITestCase):
    def test_current_user(self):
        client = create_account_with_permissions_and_do_authentication()
        url = reverse("account-current")

        response = client.get(path=url)
        data = response.data.get("user")

        self.assertEqual(response.status_code, HTTP_200_OK)

        # campos que devem ser retornados
        self.assertIsNot(data.get("person", False), False)
        self.assertIsNot(data.get("local_job", False), False)
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("email"))
        self.assertIsNotNone(data.get("is_active"))
        self.assertIsNotNone(data.get("is_staff"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("updated_at"))
