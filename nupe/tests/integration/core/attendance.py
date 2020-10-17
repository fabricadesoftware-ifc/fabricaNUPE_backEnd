from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.account.models import Account
from nupe.core.models import AccountAttendance, Attendance
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class AttendanceAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um atendimento no banco para retornar no list
        baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Attendance.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("attendants"))
        self.assertIsNotNone(data.get("student"))
        self.assertIsNotNone(data.get("status"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendance_reason"))
        self.assertIsNone(data.get("attendance_severity"))
        self.assertIsNone(data.get("opened_at"))
        self.assertIsNone(data.get("closed_at"))

    def test_retrieve_with_permission(self):
        # cria um atendimento no banco para detalhar suas informações
        attendance = baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do atendimento fornecido
        self.assertEqual(response.data.get("attendance_reason"), str(attendance.attendance_reason))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("attendants"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNotNone(response.data.get("opened_at"))
        self.assertIsNot(response.data.get("closed_at", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))

    def test_create_without_attendant_with_permission(self):
        # atendimento com informações válidas para conseguir criar
        attendance_reason = baker.make("core.AttendanceReason")
        student = baker.make("core.Student")

        attendance_data = {
            "attendance_reason": attendance_reason.id,
            "attendance_severity": "L",
            "student": student.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendance"])
        url = reverse("attendance-list")

        response = client.post(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance = Attendance.objects.get(pk=response.data.get("id"))
        self.assertEqual(attendance.attendance_reason, attendance_reason)
        self.assertEqual(Attendance.objects.count(), 1)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_create_with_one_attendant_with_permission(self):
        # atendimento com informações válidas para conseguir criar
        attendance_reason = baker.make("core.AttendanceReason")
        attendant = baker.make("account.Account")
        student = baker.make("core.Student")

        attendance_data = {
            "attendance_reason": attendance_reason.id,
            "attendance_severity": "L",
            "attendants": [attendant.id],
            "student": student.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendance"])
        url = reverse("attendance-list")

        response = client.post(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance = Attendance.objects.get(pk=response.data.get("id"))
        self.assertEqual(attendance.attendants.all().first(), attendant)
        self.assertEqual(Attendance.objects.count(), 1)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_create_with_more_than_one_attendant_with_permission(self):
        # atendimento com informações válidas para conseguir criar
        attendance_reason = baker.make("core.AttendanceReason")
        attendants = baker.make("account.Account", _quantity=2)
        student = baker.make("core.Student")

        attendance_data = {
            "attendance_reason": attendance_reason.id,
            "attendance_severity": "L",
            "attendants": [attendants[0].id, attendants[1].id],
            "student": student.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendance"])
        url = reverse("attendance-list")

        response = client.post(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance = Attendance.objects.get(pk=response.data.get("id"))
        self.assertEqual(list(attendance.attendants.all()), attendants)
        self.assertEqual(Attendance.objects.count(), 1)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_partial_update_without_attendant_with_permission(self):
        # cria um atendimento para conseguir atualiza-lo
        attendance = baker.make(Attendance)

        # somente um campo e com informação válida para conseguir atualizar
        new_attendance_severity = "H"
        attendance_data = {"attendance_severity": new_attendance_severity}

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.patch(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Attendance.objects.get(pk=attendance.id).attendance_severity, new_attendance_severity)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_partial_update_with_one_attendant_with_permission(self):
        # cria um atendimento para conseguir atualiza-lo
        attendance = baker.make(Attendance)

        new_attendant = baker.make("account.Account")

        attendance_data = {
            "attendants": [new_attendant.id],
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.patch(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Attendance.objects.get(pk=attendance.id).attendants.all().first(), new_attendant)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_partial_update_with_more_than_one_attendant_with_permission(self):
        # cria um atendimento para conseguir atualiza-lo
        attendance = baker.make(Attendance)

        new_attendants = baker.make("account.Account", _quantity=2)

        attendance_data = {
            "attendants": [new_attendants[0].id, new_attendants[1].id],
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.patch(path=url, data=attendance_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(list(Attendance.objects.get(pk=attendance.id).attendants.all()), new_attendants)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))

    def test_destroy_with_permission(self):
        # cria um atendimento no banco para conseguir mascara-lo
        attendance = baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser mascarado
        self.assertEqual(Attendance.objects.count(), 0)

        # mas deve ser mantido no banco de dados
        self.assertEqual(Attendance.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance-list")
        response = client.post(path=url, data={})

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("attendance-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_report_with_permission(self):
        # cria um atendimento no banco para retornar no report
        baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-report")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Attendance.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("attendance_reason"))
        self.assertIsNotNone(data.get("attendance_severity"))
        self.assertIsNotNone(data.get("student"))
        self.assertIsNotNone(data.get("account_attendance"))
        self.assertIsNotNone(data.get("status"))
        self.assertIsNotNone(data.get("opened_at"))
        self.assertIsNot(data.get("closed_at", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendants"))
        self.assertIsNone(data.get("account_attendances"))

    def test_my_attendances(self):
        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-my")

        # cria um atendimento no banco para retornar no report
        baker.make(AccountAttendance, account=Account.objects.all().first())

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), AccountAttendance.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNot(data.get("public_annotation", False), False)
        self.assertIsNot(data.get("private_annotation", False), False)
        self.assertIsNot(data.get("group_annotation", False), False)
        self.assertIsNotNone(data.get("attendance"))
        self.assertIsNotNone(data.get("attendance_at"))
        self.assertIsNotNone(data.get("updated_at"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("account"))
