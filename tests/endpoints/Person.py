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
from resources.const.datas.Person import BIRTHDAY_DATE, CPF, FIRST_NAME, GENDER, LAST_NAME, RG
from tests.endpoints.setup.Person import create_person
from tests.endpoints.setup.User import create_user_and_do_authentication


class PersonAPITestCase(APITestCase):
    def test_list_person_with_permission(self):
        create_person()  # cria uma pessoa no banco para retornar no list

        client = create_user_and_do_authentication(permissions=["core.view_person"])

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados
        self.assertEqual(len(response.data), Person.objects.all().count())

    def test_retrieve_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para detalhar suas informações

        client = client = create_user_and_do_authentication(permissions=["core.view_person"])

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

        client = create_user_and_do_authentication(permissions=["core.add_person"])

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("cpf"), person.get("cpf"))
        self.assertEqual(Person.objects.all().count(), 1)  # deve ser criado no banco de dados

    def test_update_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder atualizar suas informações

        # informações válidas para conseguir atualizar
        person_update = {
            "first_name": "primeiro nome atualizado",
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        client = create_user_and_do_authentication(permissions=["core.change_person"])

        url = reverse("person-detail", args=[person.id])
        response = client.put(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se atualizou no banco de dados
        self.assertEqual(Person.objects.get(id=person.id).first_name, person_update.get("first_name"))

    def test_delete_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder excluir

        client = create_user_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[person.id])
        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.all().count(), 1)

    def test_list_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_update_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-detail", args=[99])
        response = client.put(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_delete_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.view_person"])

        url = reverse("person-detail", args=[99])  # qualquer id, o banco de dados para test é vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_update_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.change_person"])

        url = reverse("person-detail", args=[99])
        response = client.put(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
