import os

from django.urls import reverse
from model_bakery import baker
from PIL import Image
from rest_framework.test import APITestCase

from nupe.file.models import ProfileImage
from resources.const.datas.image_upload import PROFILE_IMAGE_INVALID_FILENAME, PROFILE_IMAGE_VALID_FILENAME
from tests.integration_tests.endpoints.setup.user import create_user_with_permissions_and_do_authentication
from tests.remove_image_files_after_test import remove_all_files_in_dir


class ProfileImageAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # cria uma imagem qualquer
        with Image.new("RGB", (100, 100), color="blue") as new_image:
            new_image.save(PROFILE_IMAGE_VALID_FILENAME, "JPEG")

        # cria um arquivo txt não vazio qualquer
        with open(PROFILE_IMAGE_INVALID_FILENAME, "w") as invalid_image:
            invalid_image.write("foo bar")

    @classmethod
    def tearDownClass(cls):
        # remove os arquivos criados que são necessários para os testes
        os.remove(PROFILE_IMAGE_VALID_FILENAME)
        os.remove(PROFILE_IMAGE_INVALID_FILENAME)

        remove_all_files_in_dir()

    def test_create_profile_image_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("image-list")

        with open(PROFILE_IMAGE_VALID_FILENAME, "rb") as image:
            # image é um arquivo png
            profile_image_data = {"image": image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.data.get("url"))
            self.assertEqual(ProfileImage.objects.count(), 1)  # deve ser criado no banco

            # a midia deve ser criada no diretório "media/"
            profile_image_pk = response.data.get("id")
            profile_image_path = ProfileImage.objects.get(pk=profile_image_pk).image.path

            self.assertIs(os.path.exists(profile_image_path), True)

    def test_destroy_profile_image_with_permission(self):
        profile_image = baker.make(ProfileImage, _create_files=True)

        client = create_user_with_permissions_and_do_authentication(permissions=["file.delete_profileimage"])
        url = reverse("image-detail", args=[profile_image.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(ProfileImage.objects.count(), 0)
        self.assertIs(os.path.exists(profile_image.image.path), False)

    def test_destroy_profile_image_not_found_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.delete_profileimage"])
        url = reverse("image-detail", args=[99])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 404)

    def test_create_profile_image_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("image-list")

        response = client.post(path=url)

        self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_destroy_profile_image_without_permission(self):
        client = create_user_with_permissions_and_do_authentication()
        url = reverse("image-detail", args=[99])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_create_invalid_profile_image_with_permission(self):
        client = create_user_with_permissions_and_do_authentication(permissions=["file.add_profileimage"])
        url = reverse("image-list")

        with open(PROFILE_IMAGE_INVALID_FILENAME, "rb") as invalid_image:
            # invalid_image é um arquivo txt
            profile_image_data = {"image": invalid_image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            # deve retornar um erro avisando que é um arquivo de imagem inválido
            self.assertEqual(response.status_code, 400)
            self.assertIsNotNone(response.data.get("image"))
            self.assertEqual(ProfileImage.objects.count(), 0)  # não deve ser criado no banco
