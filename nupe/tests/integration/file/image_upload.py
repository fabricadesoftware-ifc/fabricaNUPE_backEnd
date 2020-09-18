import os

from django.urls import reverse
from rest_framework.test import APITestCase

from nupe.file.models import ProfileImage
from nupe.resources.datas.file.image_upload import PROFILE_IMAGE_INVALID, PROFILE_IMAGE_PNG
from nupe.tests.integration.core.setup.user import create_user_with_permissions_and_do_authentication
from nupe.tests.utils import (
    create_image,
    create_invalid_image,
    mock_profile_image,
    remove_all_files_in_dir,
    remove_images,
)


class ProfileImageAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        create_image()
        create_invalid_image()

    @classmethod
    def tearDownClass(cls):
        remove_images(paths=[PROFILE_IMAGE_PNG, PROFILE_IMAGE_INVALID])
        remove_all_files_in_dir()

    def test_create_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("profile_image-list")

        with open(PROFILE_IMAGE_PNG, "rb") as image:
            # image é um arquivo png
            profile_image_data = {"image": image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.data.get("attachment_id"))
            self.assertEqual(ProfileImage.objects.count(), 1)  # deve ser criado no banco

            # a midia deve ser criada no diretório "media/"
            profile_image_pk = response.data.get("id")
            profile_image_path = ProfileImage.objects.get(pk=profile_image_pk).image.path

            self.assertIs(os.path.exists(profile_image_path), True)

    def test_destroy_with_permission(self):
        mocked_image = mock_profile_image()

        client = create_user_with_permissions_and_do_authentication(permissions=["file.delete_profileimage"])
        url = reverse("profile_image-detail", args=[mocked_image.attachment_id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(ProfileImage.objects.count(), 0)
        self.assertIs(os.path.exists(mocked_image.image.path), False)

    def test_destroy_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.delete_profileimage"])
        url = reverse("profile_image-detail", args=[99])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 404)

    def test_create_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("profile_image-list")

        response = client.post(path=url)

        self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_destroy_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("profile_image-detail", args=[99])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_create_invalid_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("profile_image-list")

        with open(PROFILE_IMAGE_INVALID, "rb") as invalid_image:
            # invalid_image é um arquivo txt
            profile_image_data = {"image": invalid_image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            # deve retornar um erro avisando que é um arquivo de imagem inválido
            self.assertEqual(response.status_code, 400)
            self.assertIsNotNone(response.data.get("image"))
            self.assertEqual(ProfileImage.objects.count(), 0)  # não deve ser criado no banco
