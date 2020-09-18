from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import AcademicEducation, Course, Grade
from nupe.resources.datas.core.course import COURSE_NAME, GRADE_NAME
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication


class CourseAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Course)  # cria um curso no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_course"])
        url = reverse("course-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Course.objects.count())

    def test_retrieve_with_permission(self):
        course = baker.make(Course)  # cria um curso no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_course"])
        url = reverse("course-detail", args=[course.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do curso fornecido
        self.assertEqual(response.data.get("name"), course.name)

    def test_create_with_permission(self):
        # curso com informações válidas para conseguir criar
        course = {"name": COURSE_NAME}

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_course"])
        url = reverse("course-list")

        response = client.post(path=url, data=course)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), course.get("name"))
        self.assertEqual(Course.objects.count(), 1)  # deve ser criado no banco de dados

    def test_partial_update_with_permission(self):
        course = baker.make(Course)  # cria um curso no banco para poder atualizar suas informações

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

    def test_destroy_with_permission(self):
        course = baker.make(Course)  # cria um curso no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_course"])
        url = reverse("course-detail", args=[course.id])

        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("course-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_course"])

        url = reverse("course-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_course"])

        url = reverse("course-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_course"])

        url = reverse("course-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class GradeAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(Grade)  # cria um grau no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), Grade.objects.count())

    def test_retrieve_with_permission(self):
        grade = baker.make(Grade)  # cria um grau no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do grau fornecido
        self.assertEqual(response.data.get("name"), grade.name)

    def test_create_with_permission(self):
        # grau com informações válidas para conseguir criar
        grade = {"name": GRADE_NAME}

        client = create_user_with_permissions_and_do_authentication(permissions=["core.add_grade"])
        url = reverse("grade-list")

        response = client.post(path=url, data=grade)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), grade.get("name"))
        self.assertEqual(Grade.objects.count(), 1)  # deve ser criado no banco de dados

    def test_partial_update_with_permission(self):
        grade = baker.make(Grade)  # cria um grau no banco para poder atualizar suas informações

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

    def test_destroy_with_permission(self):
        grade = baker.make(Grade)  # cria um grau no banco para poder excluir

        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_grade"])
        url = reverse("grade-detail", args=[grade.id])

        response = client.delete(path=url)

        # o dado deve ser mascarado
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Grade.objects.count(), 0)

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-list")
        response = client.post(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("grade-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_grade"])

        url = reverse("grade-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.change_grade"])

        url = reverse("grade-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.delete_grade"])

        url = reverse("grade-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class AcademicEducationAPITestCase(APITestCase):
    def test_list_with_permission(self):
        baker.make(AcademicEducation)  # cria uma formação acadêmica no banco para retornar no list

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados do banco de dados não mascarados
        self.assertEqual(response.data.get("count"), AcademicEducation.objects.count())

    def test_retrieve_with_permission(self):
        academic_education = baker.make(
            AcademicEducation
        )  # cria uma formação acadêmica no banco para detalhar suas informações

        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])
        url = reverse("academic_education-detail", args=[academic_education.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da formação acadêmica fornecida
        self.assertEqual(response.data.get("name"), str(academic_education))

    def test_list_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("academic_education-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()

        url = reverse("academic_education-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["core.view_academiceducation"])

        url = reverse("academic_education-detail", args=[99])  # não existe no banco de teste porque inicia-se vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe
