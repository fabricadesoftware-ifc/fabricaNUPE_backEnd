from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.account.models import Account
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class AccountAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma conta no banco para retornar no list
        baker.make(Account)

        client = create_account_with_permissions_and_do_authentication(permissions=["account.view_account"])
        url = reverse("account-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Account.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNot(data.get("full_name", False), False)
        self.assertIsNot(data.get("local_job", False), False)
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("email"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("person"))
        self.assertIsNone(response.data.get("function"))
        self.assertIsNone(response.data.get("sector"))
        self.assertIsNone(response.data.get("date_joined"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("is_active"))
        self.assertIsNone(response.data.get("is_staff"))
        self.assertIsNone(response.data.get("is_superuser"))
        self.assertIsNone(response.data.get("short_name"))

    def test_retrieve_with_permission(self):
        # cria uma conta no banco para detalhar suas informações
        account = baker.make(Account)

        client = create_account_with_permissions_and_do_authentication(permissions=["account.view_account"])
        url = reverse("account-detail", args=[account.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da conta do email fornecido
        self.assertEqual(response.data.get("email"), account.email)

        # campos que devem ser retornados
        self.assertIsNot(response.data.get("person", False), False)
        self.assertIsNot(response.data.get("local_job", False), False)
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("email"))
        self.assertIsNotNone(response.data.get("function"))
        self.assertIsNotNone(response.data.get("sector"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("date_joined"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("is_active"))
        self.assertIsNone(response.data.get("is_staff"))
        self.assertIsNone(response.data.get("is_superuser"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("short_name"))

    def test_create_with_permission(self):
        person = baker.make("core.Person")
        local_job = baker.make("core.InstitutionCampus")
        function = baker.make("core.Function")
        sector = baker.make("core.Sector")

        # conta com informações válidas para conseguir criar
        new_account_email = "somemail@example.com"
        account = {
            "email": new_account_email,
            "person": person.id,
            "local_job": local_job.id,
            "function": function.id,
            "sector": sector.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["account.add_account"])
        url = reverse("account-list")

        response = client.post(path=url, data=account)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        account_object_model = Account.objects.get(email=new_account_email)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(account_object_model.email, new_account_email)
        self.assertEqual(account_object_model.person, person)
        self.assertEqual(account_object_model.local_job, local_job)
        self.assertEqual(account_object_model.function, function)
        self.assertEqual(account_object_model.sector, sector)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("email"))
        self.assertIsNotNone(response.data.get("person"))
        self.assertIsNotNone(response.data.get("local_job"))
        self.assertIsNotNone(response.data.get("function"))
        self.assertIsNotNone(response.data.get("sector"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("date_joined"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("is_active"))
        self.assertIsNone(response.data.get("is_staff"))
        self.assertIsNone(response.data.get("is_superuser"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("short_name"))

    def test_partial_update_with_permission(self):
        # cria uma conta no banco para conseguir atualizar suas informações
        account = baker.make(Account)

        client = create_account_with_permissions_and_do_authentication(permissions=["account.change_account"])
        url = reverse("account-detail", args=[account.id])

        new_email = "emailupdated@example.com"
        account_update = {
            "email": new_email,
        }

        response = client.patch(path=url, data=account_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Account.objects.get(pk=account.id).email, new_email)

        # campos que devem ser retornados
        self.assertIsNot(response.data.get("person", False), False)
        self.assertIsNot(response.data.get("local_job", False), False)
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("email"))
        self.assertIsNotNone(response.data.get("function"))
        self.assertIsNotNone(response.data.get("sector"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("date_joined"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("is_active"))
        self.assertIsNone(response.data.get("is_staff"))
        self.assertIsNone(response.data.get("is_superuser"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("short_name"))

    def test_destroy_with_permission(self):
        # cria uma conta no banco para conseguir excluir
        account = baker.make(Account)

        client = create_account_with_permissions_and_do_authentication(permissions=["account.delete_account"])
        url = reverse("account-detail", args=[account.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(Account.objects.count(), 1)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Account.all_objects.count(), 2)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("account-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("account-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("account-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("account-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("account-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

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
        self.assertIsNotNone(data.get("function"))
        self.assertIsNotNone(data.get("sector"))
        self.assertIsNotNone(data.get("date_joined"))
        self.assertIsNotNone(data.get("is_active"))
        self.assertIsNotNone(data.get("is_staff"))
        self.assertIsNotNone(data.get("is_superuser"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("updated_at"))
        self.assertIsNone(data.get("full_name"))
        self.assertIsNone(data.get("short_name"))
