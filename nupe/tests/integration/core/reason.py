from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import AttendanceReason
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class AttendanceReasonAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria 5 motivos de atendimento pai no banco para retornar no list
        fathers = baker.make(AttendanceReason, _quantity=5)

        # cria 3 motivos de atendimento filho no banco que não devem ser retornados no list
        baker.make(AttendanceReason, father_reason=fathers[0], _quantity=3)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendancereason"])
        url = reverse("attendance_reason-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os motivos de atendimento pai não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), 5)

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNotNone(data.get("description"))
        self.assertIsNot(data.get("father_reason", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("sons_reasons"))

    def test_retrieve_with_permission(self):
        # cria um motivo de atendimento pai no banco para detalhar suas informações
        attendance_reason = baker.make(AttendanceReason)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendancereason"])
        url = reverse("attendance_reason-detail", args=[attendance_reason.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do motivo de atendimento pai fornecido
        self.assertEqual(response.data.get("description"), attendance_reason.description)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNot(response.data.get("father_reason", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("sons_reasons"))

    def test_create_with_permission(self):
        # motivo de atendimento pai com informações válidas para conseguir criar
        attendance_reason_name = "some attendance reason"
        attendance_reason_description = "Some description to this new attendance reason! :D"
        attendance_reason = {
            "name": attendance_reason_name,
            "description": attendance_reason_description,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendancereason"])
        url = reverse("attendance_reason-list")

        response = client.post(path=url, data=attendance_reason)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance_reason = AttendanceReason.objects.get(name=attendance_reason_name)
        self.assertEqual(AttendanceReason.objects.count(), 1)
        self.assertEqual(attendance_reason.name, attendance_reason_name)
        self.assertEqual(attendance_reason.description, attendance_reason_description)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("description"))
        self.assertIsNot(response.data.get("father_reason", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("sons_reasons"))

    def test_partial_update_with_permission(self):
        # cria um motivo de atendimento pai para conseguir atualiza-lo
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
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("description"))
        self.assertIsNot(response.data.get("father_reason", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("sons_reasons"))

    def test_destroy_with_permission(self):
        # cria um motivo de atendimento pai no banco para conseguir mascara-lo
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

    def test_filter_get_sons(self):
        # cria 5 motivos de atendimento pai no banco que não devem ser retornados no list
        fathers = baker.make(AttendanceReason, _quantity=5)

        # cria 3 motivos de atendimento filho no banco para retornar no list
        sons = baker.make(AttendanceReason, father_reason=fathers[0], _quantity=3)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendancereason"])
        url = reverse("attendance_reason-list") + f"?father_reason={fathers[0].id}"

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os motivos de atendimento filho não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), 3)

        attendance_reasons_ids = [result.get("id") for result in response.data.get("results")]
        self.assertIn(sons[0].id, attendance_reasons_ids)
        self.assertIn(sons[1].id, attendance_reasons_ids)
        self.assertIn(sons[2].id, attendance_reasons_ids)
