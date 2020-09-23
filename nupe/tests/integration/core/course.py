from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.core.models import AcademicEducation, Course, Grade
from nupe.resources.datas.core.course import COURSE_NAME, GRADE_NAME
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class CourseAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um curso no banco para retornar no list
        baker.make(Course)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_course"])
        url = reverse("course-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Course.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("grades"))
        self.assertIsNone(data.get("academic_education"))

    def test_retrieve_with_permission(self):
        # cria um curso no banco para detalhar suas informações
        course = baker.make(Course)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_course"])
        url = reverse("course-detail", args=[course.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do curso fornecido
        self.assertEqual(response.data.get("name"), course.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("grades"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_create_with_permission(self):
        # curso com informações válidas para conseguir criar
        course = {"name": COURSE_NAME}

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_course"])
        url = reverse("course-list")

        response = client.post(path=url, data=course)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.all().first().name, COURSE_NAME)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("grades"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_partial_update_with_permission(self):
        # cria um curso no banco para conseguir atualizar suas informações
        course = baker.make(Course)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_course"])
        url = reverse("course-detail", args=[course.id])

        new_name = "name updated"
        course_update = {
            "name": new_name,
        }

        response = client.patch(path=url, data=course_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Course.objects.get(pk=course.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("grades"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_destroy_with_permission(self):
        # cria um curso no banco para conseguir excluir
        course = baker.make(Course)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_course"])
        url = reverse("course-detail", args=[course.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(Course.objects.count(), 0)

        # mas deve ser mantido no banco
        self.assertEqual(Course.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class GradeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um grau no banco para retornar no list
        baker.make(Grade)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Grade.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNotNone(data.get("courses_output"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("academic_education"))

    def test_retrieve_with_permission(self):
        # cria um grau no banco para detalhar suas informações
        grade = baker.make(Grade)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do grau fornecido
        self.assertEqual(response.data.get("name"), grade.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("courses_output"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_create_with_permission(self):
        # grau com informações válidas para conseguir criar
        grade = {"name": GRADE_NAME}

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_grade"])
        url = reverse("grade-list")

        response = client.post(path=url, data=grade)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        self.assertEqual(Grade.objects.count(), 1)
        self.assertEqual(Grade.objects.all().first().name, GRADE_NAME)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("courses_output"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_partial_update_with_permission(self):
        # cria um grau no banco para conseguir atualizar suas informações
        grade = baker.make(Grade)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_grade"])
        url = reverse("grade-detail", args=[grade.id])

        new_name = "name updated"
        grade_update = {
            "name": new_name,
        }

        response = client.patch(path=url, data=grade_update)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Grade.objects.get(pk=grade.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("courses_output"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education"))

    def test_destroy_with_permission(self):
        # cria um grau no banco para conseguir excluir
        grade = baker.make(Grade)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado deve ser mascarado
        self.assertEqual(Grade.objects.count(), 0)

        # mas deve ser mantido no banco
        self.assertEqual(Grade.all_objects.count(), 1)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class AcademicEducationAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma formação acadêmica no banco para retornar no list
        baker.make(AcademicEducation)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), AcademicEducation.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("course"))
        self.assertIsNone(data.get("grade"))
        self.assertIsNone(data.get("campus"))
        self.assertIsNone(data.get("courses_campus"))

    def test_retrieve_with_permission(self):
        # cria uma formação acadêmica no banco para detalhar suas informações
        academic_education = baker.make(AcademicEducation)

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-detail", args=[academic_education.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da formação acadêmica fornecida
        self.assertEqual(response.data.get("name"), str(academic_education))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("course"))
        self.assertIsNone(response.data.get("grade"))
        self.assertIsNone(response.data.get("campus"))
        self.assertIsNone(response.data.get("courses_campus"))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("academic_education-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("academic_education-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
