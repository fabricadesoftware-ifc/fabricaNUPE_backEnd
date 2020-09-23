import os
from shutil import rmtree

from django.conf import settings
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from nupe.file.models import ProfileImage
from nupe.resources.datas.file.image_upload import PROFILE_IMAGE_INVALID, PROFILE_IMAGE_PNG
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication
from nupe.tests.utils import create_image, create_invalid_image, mock_profile_image


class ProfileImageAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        create_image()
        create_invalid_image()

    @classmethod
    def tearDownClass(cls):
        os.remove(PROFILE_IMAGE_PNG)
        rmtree(settings.MEDIA_ROOT)

    def test_create_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("profile_image-list")

        with open(PROFILE_IMAGE_PNG, "rb") as image:
            # image é um arquivo png
            profile_image_data = {"image": image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            self.assertEqual(response.status_code, HTTP_201_CREATED)

            # deve ser criado no banco
            self.assertEqual(ProfileImage.objects.count(), 1)

            # campos que devem ser retornados
            self.assertIsNotNone(response.data.get("id"))
            self.assertIsNotNone(response.data.get("attachment_id"))
            self.assertIsNotNone(response.data.get("uploaded_at"))

            # campos que não devem ser retornados
            self.assertIsNone(response.data.get("image"))

    def test_destroy_with_permission(self):
        mocked_image = mock_profile_image()

        client = create_user_with_permissions_and_do_authentication(permissions=["file.delete_profileimage"])
        url = reverse("profile_image-detail", args=[mocked_image.attachment_id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # deve ser removido do banco
        self.assertEqual(ProfileImage.objects.count(), 0)

    def test_create_invalid_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("profile_image-list")

        with open(PROFILE_IMAGE_INVALID, "rb") as invalid_image:
            # invalid_image é um arquivo txt
            profile_image_data = {"image": invalid_image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

            # deve emitir mensagem de erro do campo inválido
            self.assertIsNotNone(response.data.get("image"))

            # campos que não devem ser retornados
            self.assertIsNone(response.data.get("id"))
            self.assertIsNone(response.data.get("attachment_id"))
            self.assertIsNone(response.data.get("uploaded_at"))

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("profile_image-list")

        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("profile_image-detail", args=[99])

        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
