from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import AttendanceReason, CrisisType, DrugType, SpecialNeedType
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class SpecialNeedTypeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um tipo de necessidade especial no banco para retornar no list
        baker.make(SpecialNeedType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_specialneedtype"])
        url = reverse("special_need_type-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), SpecialNeedType.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNot(data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendances"))

    def test_retrieve_with_permission(self):
        # cria um tipo de necessidade especial no banco para detalhar suas informações
        special_need_type = baker.make(SpecialNeedType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_specialneedtype"])
        url = reverse("special_need_type-detail", args=[special_need_type.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do tipo de necessidade especial fornecido
        self.assertEqual(response.data.get("name"), special_need_type.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_create_with_permission(self):
        # tipo de necessidade especial com informações válidas para conseguir criar
        special_need_type_name = "somespecialneed"
        special_need_type = {
            "name": special_need_type_name,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_specialneedtype"])
        url = reverse("special_need_type-list")

        response = client.post(path=url, data=special_need_type)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        special_need_type = SpecialNeedType.objects.get(name=special_need_type_name)
        self.assertEqual(SpecialNeedType.objects.count(), 1)
        self.assertEqual(special_need_type.name, special_need_type_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_partial_update_with_permission(self):
        # cria um tipo de necessidade especial para conseguir atualiza-lo
        special_need_type = baker.make(SpecialNeedType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_specialneedtype"])
        url = reverse("special_need_type-detail", args=[special_need_type.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_name = "nameupdated"
        special_need_type_data = {"name": new_name}

        response = client.patch(path=url, data=special_need_type_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(SpecialNeedType.objects.get(pk=special_need_type.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_destroy_with_permission(self):
        # cria um tipo de necessidade especial no banco para conseguir mascara-lo
        special_need_type = baker.make(SpecialNeedType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_specialneedtype"])
        url = reverse("special_need_type-detail", args=[special_need_type.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(SpecialNeedType.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(SpecialNeedType.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("special_need_type-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("special_need_type-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("special_need_type-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("special_need_type-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("special_need_type-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class CrisisTypeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um tipo de crise no banco para retornar no list
        baker.make(CrisisType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_crisistype"])
        url = reverse("crisis_type-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), CrisisType.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNot(data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendances"))

    def test_retrieve_with_permission(self):
        # cria um tipo de crise no banco para detalhar suas informações
        crisis_type = baker.make(CrisisType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_crisistype"])
        url = reverse("crisis_type-detail", args=[crisis_type.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do tipo de crise fornecido
        self.assertEqual(response.data.get("name"), crisis_type.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_create_with_permission(self):
        # tipo de crise com informações válidas para conseguir criar
        crisis_type_name = "somecrisistype"
        crisis_type = {
            "name": crisis_type_name,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_crisistype"])
        url = reverse("crisis_type-list")

        response = client.post(path=url, data=crisis_type)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        crisis_type = CrisisType.objects.get(name=crisis_type_name)
        self.assertEqual(CrisisType.objects.count(), 1)
        self.assertEqual(crisis_type.name, crisis_type_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_partial_update_with_permission(self):
        # cria um tipo de crise para conseguir atualiza-lo
        crisis_type = baker.make(CrisisType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_crisistype"])
        url = reverse("crisis_type-detail", args=[crisis_type.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_name = "nameupdated"
        crisis_type_data = {"name": new_name}

        response = client.patch(path=url, data=crisis_type_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(CrisisType.objects.get(pk=crisis_type.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_destroy_with_permission(self):
        # cria um tipo de crise no banco para conseguir mascara-lo
        crisis_type = baker.make(CrisisType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_crisistype"])
        url = reverse("crisis_type-detail", args=[crisis_type.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(CrisisType.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(CrisisType.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("crisis_type-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("crisis_type-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("crisis_type-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("crisis_type-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("crisis_type-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class DrugTypeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um tipo de droga no banco para retornar no list
        baker.make(DrugType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_drugtype"])
        url = reverse("drug_type-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), DrugType.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNot(data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendances"))

    def test_retrieve_with_permission(self):
        # cria um tipo de droga no banco para detalhar suas informações
        drug_type = baker.make(DrugType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_drugtype"])
        url = reverse("drug_type-detail", args=[drug_type.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do tipo de droga fornecido
        self.assertEqual(response.data.get("name"), drug_type.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_create_with_permission(self):
        # tipo de droga com informações válidas para conseguir criar
        drug_type_name = "somedrugtype"
        drug_type = {
            "name": drug_type_name,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_drugtype"])
        url = reverse("drug_type-list")

        response = client.post(path=url, data=drug_type)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        drug_type = DrugType.objects.get(name=drug_type_name)
        self.assertEqual(DrugType.objects.count(), 1)
        self.assertEqual(drug_type.name, drug_type_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_partial_update_with_permission(self):
        # cria um tipo de droga para conseguir atualiza-lo
        drug_type = baker.make(DrugType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_drugtype"])
        url = reverse("drug_type-detail", args=[drug_type.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_name = "nameupdated"
        drug_type_data = {"name": new_name}

        response = client.patch(path=url, data=drug_type_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(DrugType.objects.get(pk=drug_type.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("description", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("attendances"))

    def test_destroy_with_permission(self):
        # cria um tipo de droga no banco para conseguir mascara-lo
        drug_type = baker.make(DrugType)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_drugtype"])
        url = reverse("drug_type-detail", args=[drug_type.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(DrugType.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(DrugType.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("drug_type-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("drug_type-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("drug_type-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("drug_type-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("drug_type-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class AttendanceReasonAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um motivo de atendimento no banco para retornar no list
        baker.make(AttendanceReason)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendancereason"])
        url = reverse("attendance_reason-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), AttendanceReason.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("description"))
        self.assertIsNotNone(data.get("special_need"))
        self.assertIsNotNone(data.get("crisis"))
        self.assertIsNotNone(data.get("drug"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))

    def test_retrieve_with_permission(self):
        # cria um motivo de atendimento no banco para detalhar suas informações
        attendance_reason = baker.make(AttendanceReason)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendancereason"])
        url = reverse("attendance_reason-detail", args=[attendance_reason.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do motivo de atendimento fornecido
        self.assertEqual(response.data.get("description"), attendance_reason.description)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("special_need"))
        self.assertIsNotNone(response.data.get("crisis"))
        self.assertIsNotNone(response.data.get("drug"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))

    def test_create_with_permission(self):
        special_need_type = baker.make(SpecialNeedType)
        crisis_type = baker.make(CrisisType)
        drug_type = baker.make(DrugType)

        # motivo de atendimento com informações válidas para conseguir criar
        attendance_reason_description = "Some description to this new attendance reason! :D"
        attendance_reason = {
            "description": attendance_reason_description,
            "special_need": [special_need_type.id],
            "crisis": [crisis_type.id],
            "drug": [drug_type.id],
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendancereason"])
        url = reverse("attendance_reason-list")

        response = client.post(path=url, data=attendance_reason)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance_reason = AttendanceReason.objects.get(description=attendance_reason_description)
        self.assertEqual(AttendanceReason.objects.count(), 1)
        self.assertEqual(attendance_reason.description, attendance_reason_description)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("description"))
        self.assertIsNotNone(response.data.get("special_need"))
        self.assertIsNotNone(response.data.get("crisis"))
        self.assertIsNotNone(response.data.get("drug"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))

    def test_partial_update_with_permission(self):
        # cria um motivo de atendimento para conseguir atualiza-lo
        attendance_reason = baker.make(AttendanceReason)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_attendancereason"])
        url = reverse("attendance_reason-detail", args=[attendance_reason.id])

        # somente um campo e com informação válida para conseguir atualizar
        new_description = "Description is now updated! xD"
        attendance_reason_data = {"description": new_description}

        response = client.patch(path=url, data=attendance_reason_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(AttendanceReason.objects.get(pk=attendance_reason.id).description, new_description)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("description"))
        self.assertIsNotNone(response.data.get("special_need"))
        self.assertIsNotNone(response.data.get("crisis"))
        self.assertIsNotNone(response.data.get("drug"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))

    def test_destroy_with_permission(self):
        # cria um motivo de atendimento no banco para conseguir mascara-lo
        attendance_reason = baker.make(AttendanceReason)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_attendancereason"])
        url = reverse("attendance_reason-detail", args=[attendance_reason.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(AttendanceReason.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(AttendanceReason.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance_reason-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance_reason-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance_reason-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance_reason-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance_reason-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
