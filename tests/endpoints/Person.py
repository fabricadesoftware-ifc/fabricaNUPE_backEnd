from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import Person
from tests.endpoints.setup import (
    BIRTHDAY_DATE,
    CPF,
    FIRST_NAME,
    GENDER,
    LAST_NAME,
    RG,
    create_person,
    create_user_with_permissions,
)


class PersonAPITestCase(APITestCase):
    def test_list_person_with_permission(self):
        create_person()  # cria uma pessoa no banco para retornar no list

        client = self.client  # instancia de APIClient

        user = create_user_with_permissions(username="teste", permissions=["core.view_person"])
        client.force_authenticate(user=user)

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados
        self.assertEqual(len(response.data), Person.objects.all().count())

    def test_retrieve_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para detalhar suas informações

        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.view_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[person.id])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do usuário do id fornecido
        self.assertEqual(response.data.get("id"), person.id)

    def test_create_person_with_permission(self):
        # pessoa com informações válidas para conseguir criar
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.add_person"])
        client.force_authenticate(user=user)

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("cpf"), person.get("cpf"))
        self.assertEqual(Person.objects.all().count(), 1)  # deve ser criado no banco de dados

    def test_update_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder atualizar suas informações

        # informações válidas para conseguir atualizar
        person_update = {
            "first_name": LAST_NAME,
            "last_name": FIRST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.change_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[person.id])
        response = client.put(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se atualizou no banco de dados
        self.assertEqual(Person.objects.get(id=person.id).first_name, person_update.get("first_name"))

    def test_delete_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder excluir

        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.delete_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[person.id])
        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.all().count(), 1)

    def test_list_person_without_permission(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=[])
        client.force_authenticate(user=user)

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_person_without_permission(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=[])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[1])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_person_without_permission(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=[])
        client.force_authenticate(user=user)

        url = reverse("person-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_update_person_without_permission(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=[])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[1])
        response = client.put(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_delete_person_without_permission(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=[])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[1])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_id_not_found(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.view_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[99])  # qualquer id, o banco de dados para test é vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_update_id_not_found(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.change_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[99])
        response = client.put(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_id_not_found(self):
        client = self.client

        user = create_user_with_permissions(username="teste", permissions=["core.delete_person"])
        client.force_authenticate(user=user)

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
