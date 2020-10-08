from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import Function, Sector
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class FuctionAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma função/cargo no banco para retornar no list
        baker.make(Function)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_function"])
        url = reverse("function-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Function.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNot(data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("workers"))

    def test_retrieve_with_permission(self):
        # cria uma função/cargo no banco para detalhar suas informações
        function = baker.make(Function)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_function"])
        url = reverse("function-detail", args=[function.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da função/cargo fornecida
        self.assertEqual(response.data.get("name"), function.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_create_with_permission(self):
        # função/cargo com informações válidas para conseguir criar
        function_name = "somefunction"
        function_data = {
            "name": function_name,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_function"])
        url = reverse("function-list")

        response = client.post(path=url, data=function_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        function = Function.objects.get(name=function_name)
        self.assertEqual(function.name, function_name)

        # uma função/cargo é criada em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Function.objects.count(), 2)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_partial_update_with_permission(self):
        # cria uma função/cargo para conseguir atualiza-lo
        function = baker.make(Function)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_function"])
        url = reverse("function-detail", args=[function.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_name = "nameupdated"
        function_update_data = {"name": new_name}

        response = client.patch(path=url, data=function_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Function.objects.get(pk=function.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_destroy_with_permission(self):
        # cria uma função/cargo no banco para conseguir mascara-lo
        function = baker.make(Function)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_function"])
        url = reverse("function-detail", args=[function.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(Function.objects.count(), 1)

        # mas deve ser mantido no banco de dados
        # uma função/cargo é criada em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Function.all_objects.count(), 2)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("function-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("function-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("function-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("function-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("function-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class SectorAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um setor no banco para retornar no list
        baker.make(Sector)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_sector"])
        url = reverse("sector-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Sector.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNot(data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("workers"))

    def test_retrieve_with_permission(self):
        # cria um setor no banco para detalhar suas informações
        sector = baker.make(Sector)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_sector"])
        url = reverse("sector-detail", args=[sector.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do setor fornecido
        self.assertEqual(response.data.get("name"), sector.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_create_with_permission(self):
        # setor com informações válidas para conseguir criar
        sector_name = "somesector"
        sector_data = {
            "name": sector_name,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_sector"])
        url = reverse("sector-list")

        response = client.post(path=url, data=sector_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        sector = Sector.objects.get(name=sector_name)
        self.assertEqual(sector.name, sector_name)

        # um setor é criado em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Sector.objects.count(), 2)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_partial_update_with_permission(self):
        # cria um setor para conseguir atualiza-lo
        sector = baker.make(Sector)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_sector"])
        url = reverse("sector-detail", args=[sector.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_name = "nameupdated"
        sector_update_data = {"name": new_name}

        response = client.patch(path=url, data=sector_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Sector.objects.get(pk=sector.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("workers"))

    def test_destroy_with_permission(self):
        # cria um setor no banco para conseguir mascara-lo
        sector = baker.make(Sector)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_sector"])
        url = reverse("sector-detail", args=[sector.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(Sector.objects.count(), 1)

        # mas deve ser mantido no banco de dados
        # um setor é criado em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Sector.all_objects.count(), 2)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("sector-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("sector-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("sector-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("sector-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("sector-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
