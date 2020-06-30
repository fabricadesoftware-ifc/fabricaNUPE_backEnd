from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import Person
from resources.const.datas.person import BIRTHDAY_DATE, CPF, FIRST_NAME, GENDER, LAST_NAME
from tests.integration_tests.endpoints.setup.user import create_user_with_permissions_and_do_authentication


class PersonAPITestCase(APITestCase):
    def test_list_person_with_permission(self):
        baker.make(Person)  # cria uma pessoa no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Person.objects.count())

    def test_retrieve_person_with_permission(self):
        person = baker.make(Person)  # cria uma pessoa no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do usuário do cpf fornecido
        self.assertEqual(response.data.get("cpf"), person.cpf)

    def test_create_person_with_permission(self):
        # pessoa com informações válidas para conseguir criar
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("cpf"), person.get("cpf"))
        self.assertEqual(Person.objects.count(), 1)  # deve ser criado no banco de dados

    def test_partial_update_person_with_permission(self):
        person = baker.make(Person, cpf=CPF)  # cria uma pessoa no banco para poder atualizar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        # somente um campo e com informações válidas para conseguir atualizar
        new_first_name = "first name updated"
        person_update = {"first_name": new_first_name}

        response = client.patch(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Person.objects.get(pk=person.id).first_name, new_first_name)

        # todos os campos e com informações válidas para conseguir atualizar
        new_last_name = "last name updated"

        person_update = {
            "first_name": new_first_name,
            "last_name": new_last_name,
            "cpf": person.cpf,
            "birthday_date": person.birthday_date,
            "gender": person.gender,
            "contact": person.contact,
        }

        response = client.patch(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se todos os campos atualizou no banco de dados
        person_database = Person.objects.get(pk=person.id)

        self.assertEqual(person_database.first_name, new_first_name)
        self.assertEqual(person_database.last_name, new_last_name)
        self.assertEqual(person_database.cpf, person.cpf)
        self.assertEqual(person_database.birthday_date, person.birthday_date)
        self.assertEqual(person_database.gender, person.gender)
        self.assertEqual(person_database.contact, person.contact)

    def test_destroy_person_with_permission(self):
        person = baker.make(Person)  # cria uma pessoa no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.count(), 1)

    def test_create_invalid_person_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        # first_name e last_name devem conter somente letras e espaço
        invalid_first_name = "1nv@lid"
        person_data = {
            "first_name": invalid_first_name,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("first_name"))

        invalid_cpf = "12345678910"  # o dígito verificador deve ser válido
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": invalid_cpf,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("cpf"))

        invalid_gender = "invalid_gender"  # valor válido: F ou M
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": invalid_gender,
            "birthday_date": BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("gender"))

        invalid_birthday_date = "14/02/1999"  # formato válido: yyyy-MM-dd
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": invalid_birthday_date,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("birthday_date"))

        invalid_contact = "999999999"  # deve conter 12 números. Ex: 047999999999
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
            "contact": invalid_contact,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("contact"))

    def test_partial_update_invalid_with_permission(self):
        # cria uma pessoa no banco para poder atualiza-lo
        person = baker.make(Person, cpf=CPF)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_first_name = "1nv@lid"
        person_data = {
            "first_name": invalid_first_name,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("first_name"))

        invalid_cpf = "12345678910"
        person_data = {
            "cpf": invalid_cpf,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("cpf"))

        invalid_gender = "invalid_gender"
        person_data = {
            "gender": invalid_gender,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("gender"))

        invalid_birthday_date = "14/02/1999"
        person_data = {
            "birthday_date": invalid_birthday_date,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("birthday_date"))

        invalid_contact = "999999999"
        person_data = {
            "contact": invalid_contact,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("contact"))

    def test_list_person_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_person_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_person_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_person_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_person_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_registration_not_found(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])

        url = reverse("person-detail", args=[99])  # qualquer registration, o banco de dados para test é vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_registration_not_found(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_registration_not_found(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
