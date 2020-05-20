from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
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

        url = reverse("person-list")
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados
        self.assertEqual(len(response.data), Person.objects.all().count())

    def test_retrieve_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para detalhar suas informações

        client = self.client
        user = create_user_with_permissions(username="teste", permissions=["core.view_person"])

        url = reverse("person-detail", args=[person.id])
        client.force_authenticate(user=user)
        response = client.get(url)

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

        url = reverse("person-list")
        client.force_authenticate(user=user)
        response = client.post(url, person)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("cpf"), person.get("cpf"))
        self.assertEqual(Person.objects.all().count(), 1)  # verifica se foi criado no banco de dados

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

        url = reverse("person-detail", args=[person.id])
        client.force_authenticate(user=user)
        response = client.put(url, person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se atualizou no banco de dados
        self.assertEqual(Person.objects.get(id=person.id).first_name, person_update.get("first_name"))

    def test_list_person_without_permission(self):
        client = self.client
        user = create_user_with_permissions(username="teste", permissions=[])

        url = reverse("person-list")
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_person_without_permission(self):
        person = create_person()

        client = self.client
        user = create_user_with_permissions(username="teste", permissions=[])

        url = reverse("person-detail", args=[person.id])
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_create_person_without_permission(self):
        client = self.client
        user = create_user_with_permissions(username="teste", permissions=[])

        url = reverse("person-list")
        client.force_authenticate(user=user)
        response = client.post(url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_update_person_without_permission(self):
        person = create_person()

        client = self.client
        user = create_user_with_permissions(username="teste", permissions=[])

        url = reverse("person-detail", args=[person.id])
        client.force_authenticate(user=user)
        response = client.put(url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_id_not_found(self):
        client = self.client
        user = create_user_with_permissions(username="teste", permissions=["core.view_person"])

        url = reverse("person-detail", args=[99])  # qualquer id, o banco de dados para test é vazio
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_update_id_not_found(self):
        client = self.client
        user = create_user_with_permissions(username="teste", permissions=["core.change_person"])

        url = reverse("person-detail", args=[99])
        client.force_authenticate(user=user)
        response = client.put(url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe
