from django.urls import reverse
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
from resources.const.datas.Person import (
    BIRTHDAY_DATE,
    CPF,
    CPF_2,
    CPF_3,
    FIRST_NAME,
    GENDER,
    LAST_NAME,
    RG,
    RG_2,
    RG_3,
)
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
        self.assertEqual(len(response.data.get("results")), Person.objects.all().count())

    def test_retrieve_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para detalhar suas informações

        client = client = create_user_and_do_authentication(permissions=["core.view_person"])

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

    def test_partial_update_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder atualizar suas informações

        client = create_user_and_do_authentication(permissions=["core.change_person"])

        # informações válidas para conseguir atualizar
        new_first_name = "first name updated"
        person_update = {"first_name": new_first_name}

        url = reverse("person-detail", args=[person.cpf])
        response = client.patch(path=url, data=person_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # verifica se atualizou no banco de dados
        self.assertEqual(Person.objects.get(cpf=person.cpf).first_name, new_first_name)

    def test_destroy_person_with_permission(self):
        person = create_person()  # cria uma pessoa no banco para poder excluir

        client = create_user_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[person.cpf])
        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.all().count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Person.all_objects.all().count(), 1)

    def test_create_invalid_person_with_permission(self):
        client = create_user_and_do_authentication(permissions=["core.add_person"])

        # first_name e last_name devem conter somente letras e espaço
        invalid_first_name = "1nv@lid"
        person = {
            "first_name": invalid_first_name,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertNotEqual(response.data.get("first_name"), None)

        invalid_cpf = "12345678910"  # o dígito verificador deve ser válido
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": invalid_cpf,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("cpf"), None)

        invalid_rg = "invalid_rg"  # deve conter somente números
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": invalid_rg,
            "gender": GENDER,
            "birthday_date": BIRTHDAY_DATE,
        }

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("rg"), None)

        invalid_gender = "invalid_gender"  # valor válido: F ou M
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": invalid_gender,
            "birthday_date": BIRTHDAY_DATE,
        }

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("gender"), None)

        invalid_birthday_date = "14/02/1999"  # formato válido: yyyy-MM-dd
        person = {
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "cpf": CPF,
            "rg": RG,
            "gender": GENDER,
            "birthday_date": invalid_birthday_date,
        }

        url = reverse("person-list")
        response = client.post(path=url, data=person)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("birthday_date"), None)

    def test_partial_update_invalid_with_permission(self):
        # cria uma pessoa no banco para poder atualiza-lo
        person = create_person()

        client = create_user_and_do_authentication(permissions=["core.change_person"])

        invalid_first_name = "1nv@lid"
        person_data = {
            "first_name": invalid_first_name,
        }

        url = reverse("person-detail", args=[person.cpf])
        response = client.patch(path=url, data=person_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("first_name"), None)

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

    def test_partial_update_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_person_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_registration_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.view_person"])

        url = reverse("person-detail", args=[99])  # qualquer registration, o banco de dados para test é vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_registration_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.change_person"])

        url = reverse("person-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_registration_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.delete_person"])

        url = reverse("person-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_search_filter(self):
        person1 = create_person()
        create_person(cpf=CPF_2, rg=RG_2)
        create_person(cpf=CPF_3, rg=RG_3)

        client = create_user_and_do_authentication(permissions=["core.view_person"])

        search_by_first_name = f"?search={person1.first_name}"
        url = reverse("person-list") + search_by_first_name

        response = client.get(path=url)

        # as 3 pessoas tem o mesmo nome, por isso deve retornar todos
        self.assertEqual(len(response.data.get("results")), 3)

    def test_param_filter(self):
        female_gender = "F"
        birthday_date = "2005-10-10"

        create_person(gender=female_gender, birthday_date=birthday_date)
        create_person(cpf=CPF_2, rg=RG_2, gender=female_gender)
        create_person(cpf=CPF_3, rg=RG_3)

        client = create_user_and_do_authentication(permissions=["core.view_person"])

        filter_by_gender = f"?gender={female_gender}"
        url = reverse("person-list") + filter_by_gender

        response = client.get(path=url)

        # no banco contém 2 pessoas do gênero feminino e 1 masculino
        self.assertEqual(len(response.data.get("results")), 2)

        filter_by_range_date = f"?birthday_date_after={birthday_date}"  # _after usa >= e _before usa <=
        url = reverse("person-list") + filter_by_range_date

        response = client.get(path=url)

        # só existe uma pessoa no banco que nasceu a partir de 2005-10-10
        self.assertEqual(len(response.data.get("results")), 1)

    def test_not_found_search_filter(self):
        create_person()

        client = create_user_and_do_authentication(permissions=["core.view_person"])

        search_by_first_name_not_in_database = f"?search={'not in database'}"
        url = reverse("person-list") + search_by_first_name_not_in_database

        response = client.get(path=url)

        # por não ter nenhuma pessoa com esse nome no banco de dados, deve retornar uma lista vazia
        self.assertEqual(len(response.data.get("results")), 0)

    def test_not_found_param_filter(self):
        female_gender = "F"

        create_person()
        create_person(cpf=CPF_2, rg=RG_2)

        client = create_user_and_do_authentication(permissions=["core.view_person"])

        filter_by_gender = f"?gender={female_gender}"
        url = reverse("person-list") + filter_by_gender

        response = client.get(path=url)

        # no banco contém 2 pessoas e do gênero masculino, por isso, deve retornar uma lista vazia
        self.assertEqual(len(response.data.get("results")), 0)

        filter_by_range_date = f"?birthday_date_after={'2020-06-15'}"
        url = reverse("person-list") + filter_by_range_date

        response = client.get(path=url)

        # no banco não há nenhuma pessoa que nasceu a partir de 2020-06-15, por isso, deve retornar uma lista vazia
        self.assertEqual(len(response.data.get("results")), 0)
