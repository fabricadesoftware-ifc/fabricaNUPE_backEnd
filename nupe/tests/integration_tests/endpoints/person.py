import os.path

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
from nupe.resources.const.datas.person import CPF, FIRST_NAME, GENDER, LAST_NAME, OLDER_BIRTHDAY_DATE
from nupe.tests.integration_tests.endpoints.setup.user import create_user_with_permissions_and_do_authentication
from nupe.tests.utils import mock_image


class PersonAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Person)  # cria uma pessoa no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Person.objects.count())

    def test_retrieve_with_permission(self):
        person = baker.make(Person)  # cria uma pessoa no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do usuário do cpf fornecido
        self.assertEqual(response.data.get("cpf"), person.cpf)

    def test_create_with_permission(self):
        mocked_image = mock_image()

        # pessoa com informações válidas para conseguir criar
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": OLDER_BIRTHDAY_DATE,
            "profile_image": mocked_image.attachment_id,
        }

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("cpf"), person.get("cpf"))
        self.assertEqual(Person.objects.count(), 1)  # deve ser criado no banco de dados
        self.assertIs(os.path.exists(mocked_image.image.path), True)  # deve estar no diretório

    def test_partial_update_with_permission(self):
        person = baker.make(Person)  # cria uma pessoa no banco para poder atualizar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        new_first_name = "first name updated"
        person_update = {
            "first_name": new_first_name,
        }

        response = client.patch(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Person.objects.get(pk=person.id).first_name, new_first_name)

    def test_partial_update_profile_image_with_permission(self):
        mocked_image = mock_image()
        person = baker.make(Person, profile_image=mocked_image)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        mocked_image = mock_image()
        person_update = {
            "profile_image": mocked_image.attachment_id,
        }

        # a imagem atual deve estar no diretório
        self.assertIs(os.path.exists(person.profile_image.image.path), True)

        response = client.patch(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Person.objects.get(pk=person.id).profile_image, mocked_image)

        # a imagem antiga deve ser excluída do diretório
        self.assertIs(os.path.exists(person.profile_image.image.path), False)

        # E a nova imagem deve estar no diretório, substituindo a antiga
        self.assertIs(os.path.exists(mocked_image.image.path), True)

    def test_destroy_with_permission(self):
        person = baker.make(Person)  # cria uma pessoa no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.count(), 1)

    def test_create_invalid_cpf_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        invalid_cpf = "12345678910"  # o dígito verificador deve ser válido
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": invalid_cpf,
            "gender": GENDER,
            "birthday_date": OLDER_BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("cpf"))

    def test_create_invalid_gender_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        invalid_gender = "invalid_gender"  # valor válido: F ou M
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": invalid_gender,
            "birthday_date": OLDER_BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("gender"))

    def test_create_invalid_birthday_date_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

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

    def test_create_invalid_contact_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        invalid_contact = "999999999"  # deve conter 12 números. Ex: 047999999999
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": OLDER_BIRTHDAY_DATE,
            "contact": invalid_contact,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("contact"))

    def test_partial_update_invalid_cpf_with_permission(self):
        person = baker.make(Person)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_cpf = "12345678910"
        person_data = {
            "cpf": invalid_cpf,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("cpf"))

    def test_partial_update_invalid_gender_with_permission(self):
        person = baker.make(Person)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_gender = "invalid_gender"
        person_data = {
            "gender": invalid_gender,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("gender"))

    def test_partial_update_invalid_birthday_date_with_permission(self):
        person = baker.make(Person)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_birthday_date = "14/02/1999"
        person_data = {
            "birthday_date": invalid_birthday_date,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("birthday_date"))

    def test_partial_update_invalid_contact_with_permission(self):
        person = baker.make(Person)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_contact = "999999999"
        person_data = {
            "contact": invalid_contact,
        }

        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("contact"))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_person"])

        url = reverse("person-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_person"])

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
