import os.path
from datetime import datetime

from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from nupe.core.models import Person
from nupe.resources.datas.core.person import CPF, FIRST_NAME, GENDER, LAST_NAME, OLDER_BIRTHDAY_DATE
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication
from nupe.tests.utils import mock_profile_image


class PersonAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma pessoa no banco para retornar no list
        baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Person.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("full_name"))
        self.assertIsNotNone(data.get("cpf"))
        self.assertIsNot(data.get("contact", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("first_name"))
        self.assertIsNone(response.data.get("last_name"))
        self.assertIsNone(response.data.get("birthday_date"))
        self.assertIsNone(response.data.get("gender"))
        self.assertIsNone(response.data.get("profile_image"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("age"))

    def test_retrieve_with_permission(self):
        # cria uma pessoa no banco para detalhar suas informações
        person = baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do usuário do cpf fornecido
        self.assertEqual(response.data.get("cpf"), person.cpf)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("first_name"))
        self.assertIsNotNone(response.data.get("last_name"))
        self.assertIsNotNone(response.data.get("cpf"))
        self.assertIsNotNone(response.data.get("birthday_date"))
        self.assertIsNotNone(response.data.get("gender"))
        self.assertIsNot(response.data.get("contact", False), False)
        self.assertIsNot(response.data.get("profile_image", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_create_with_permission(self):
        mocked_image = mock_profile_image()

        # pessoa com informações válidas para conseguir criar
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "gender": GENDER,
            "birthday_date": OLDER_BIRTHDAY_DATE,
            "profile_image": mocked_image.attachment_id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        person = Person.objects.get(cpf=CPF)

        # uma pessoa é criada em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Person.objects.count(), 2)

        self.assertEqual(person.first_name, FIRST_NAME)
        self.assertEqual(person.last_name, LAST_NAME)
        self.assertEqual(person.cpf, CPF)
        self.assertEqual(person.gender, GENDER)
        self.assertEqual(person.birthday_date, datetime.strptime(OLDER_BIRTHDAY_DATE, "%Y-%m-%d").date())
        self.assertEqual(person.profile_image, mocked_image)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("first_name"))
        self.assertIsNotNone(response.data.get("last_name"))
        self.assertIsNotNone(response.data.get("cpf"))
        self.assertIsNotNone(response.data.get("birthday_date"))
        self.assertIsNotNone(response.data.get("gender"))
        self.assertIsNot(response.data.get("contact", False), False)
        self.assertIsNotNone(response.data.get("profile_image"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_partial_update_with_permission(self):
        # cria uma pessoa no banco para conseguir atualizar suas informações
        person = baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        new_first_name = "first name updated"
        person_update_data = {
            "first_name": new_first_name,
        }

        response = client.patch(path=url, data=person_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Person.objects.get(pk=person.id).first_name, new_first_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("first_name"))
        self.assertIsNotNone(response.data.get("last_name"))
        self.assertIsNotNone(response.data.get("cpf"))
        self.assertIsNotNone(response.data.get("birthday_date"))
        self.assertIsNotNone(response.data.get("gender"))
        self.assertIsNot(response.data.get("contact", False), False)
        self.assertIsNot(response.data.get("profile_image", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_partial_update_profile_image_with_permission(self):
        mocked_image = mock_profile_image()
        person = baker.make(Person, profile_image=mocked_image)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        new_mocked_image = mock_profile_image()
        person_update_data = {
            "profile_image": new_mocked_image.attachment_id,
        }

        response = client.patch(path=url, data=person_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Person.objects.get(pk=person.id).profile_image, new_mocked_image)

        # a imagem antiga deve ser excluída do diretório
        self.assertIs(os.path.exists(mocked_image.image.path), False)

        # E a nova imagem deve estar no diretório, substituindo a antiga
        self.assertIs(os.path.exists(new_mocked_image.image.path), True)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("first_name"))
        self.assertIsNotNone(response.data.get("last_name"))
        self.assertIsNotNone(response.data.get("cpf"))
        self.assertIsNotNone(response.data.get("birthday_date"))
        self.assertIsNotNone(response.data.get("gender"))
        self.assertIsNot(response.data.get("contact", False), False)
        self.assertIsNotNone(response.data.get("profile_image"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_destroy_with_permission(self):
        # cria uma pessoa no banco para conseguir excluir
        person = baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_person"])
        url = reverse("person-detail", args=[person.cpf])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(Person.objects.count(), 1)

        # mas deve ser mantido no banco de dados
        # uma pessoa é criada em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
        self.assertEqual(Person.all_objects.count(), 2)

    def test_create_invalid_cpf_with_permission(self):
        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        invalid_cpf = "12345678910"
        person_data = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": invalid_cpf,
            "gender": GENDER,
            "birthday_date": OLDER_BIRTHDAY_DATE,
        }

        response = client.post(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("cpf"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("first_name"))
        self.assertIsNone(response.data.get("last_name"))
        self.assertIsNone(response.data.get("birthday_date"))
        self.assertIsNone(response.data.get("gender"))
        self.assertIsNone(response.data.get("contact"))
        self.assertIsNone(response.data.get("profile_image"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_create_invalid_contact_with_permission(self):
        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_person"])
        url = reverse("person-list")

        invalid_contact = "999999999"
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

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("contact"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("first_name"))
        self.assertIsNone(response.data.get("last_name"))
        self.assertIsNone(response.data.get("cpf"))
        self.assertIsNone(response.data.get("birthday_date"))
        self.assertIsNone(response.data.get("gender"))
        self.assertIsNone(response.data.get("profile_image"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_partial_update_invalid_cpf_with_permission(self):
        person = baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_cpf = "12345678910"
        person_update_data = {
            "cpf": invalid_cpf,
        }

        response = client.patch(path=url, data=person_update_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("cpf"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("first_name"))
        self.assertIsNone(response.data.get("last_name"))
        self.assertIsNone(response.data.get("birthday_date"))
        self.assertIsNone(response.data.get("gender"))
        self.assertIsNone(response.data.get("contact"))
        self.assertIsNone(response.data.get("profile_image"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_partial_update_invalid_contact_with_permission(self):
        person = baker.make(Person)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_person"])
        url = reverse("person-detail", args=[person.cpf])

        invalid_contact = "999999999"
        person_update_data = {
            "contact": invalid_contact,
        }

        response = client.patch(path=url, data=person_update_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertIsNotNone(response.data.get("contact"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("first_name"))
        self.assertIsNone(response.data.get("last_name"))
        self.assertIsNone(response.data.get("cpf"))
        self.assertIsNone(response.data.get("birthday_date"))
        self.assertIsNone(response.data.get("gender"))
        self.assertIsNone(response.data.get("profile_image"))
        self.assertIsNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("student_registrations"))
        self.assertIsNone(response.data.get("dependents"))
        self.assertIsNone(response.data.get("responsibles"))
        self.assertIsNone(response.data.get("full_name"))
        self.assertIsNone(response.data.get("age"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("person-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
