from os import path, remove

from django.core.files.images import ImageFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from nupe.file.models import ProfileImage
from resources.const.datas.image_upload import PROFILE_IMAGE_INVALID_FILENAME, PROFILE_IMAGE_VALID_FILENAME
from tests.endpoints.setup.user import create_user_and_do_authentication


class ProfileImageAPITestCase(APITestCase):
    def tearDown(self):
        if path.exists(PROFILE_IMAGE_VALID_FILENAME):
            remove(PROFILE_IMAGE_VALID_FILENAME)

        if path.exists(PROFILE_IMAGE_INVALID_FILENAME):
            remove(PROFILE_IMAGE_INVALID_FILENAME)

    def setUp(self):
        # cria uma imagem qualquer
        new_image = Image.new("RGB", (100, 100), color="blue")
        new_image.save(PROFILE_IMAGE_VALID_FILENAME)

        # cria um arquivo txt não vazio qualquer
        with open(PROFILE_IMAGE_INVALID_FILENAME, "w") as invalid_image:
            invalid_image.write("foo bar")

    def test_create_profile_image_with_permission(self):
        client = create_user_and_do_authentication(permissions=["file.add_profileimage"])

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

            self.assertTrue(path.exists(profile_image_path))

            remove(profile_image_path)  # remove o arquivo criado no diretório "media/"

    def test_destroy_profile_image_with_permission(self):
        with open(PROFILE_IMAGE_VALID_FILENAME, "rb") as image:
            image = ImageFile(image)

            profile_image = ProfileImage.objects.create(image=image)

            client = create_user_and_do_authentication(permissions=["file.delete_profileimage"])
            url = reverse("image-detail", args=[profile_image.id])

            response = client.delete(path=url)

            self.assertEqual(response.status_code, 204)
            self.assertEqual(ProfileImage.objects.count(), 0)
            self.assertFalse(path.exists(profile_image.image.path))

    def test_create_profile_image_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("image-list")

        with open(PROFILE_IMAGE_VALID_FILENAME, "rb") as image:
            profile_image_data = {"image": image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_destroy_profile_image_without_permission(self):
        with open(PROFILE_IMAGE_VALID_FILENAME, "rb") as image:
            image = ImageFile(image)

            profile_image = ProfileImage.objects.create(image=image)

            client = create_user_and_do_authentication(permissions=[])
            url = reverse("image-detail", args=[profile_image.id])

            response = client.delete(path=url)

            self.assertEqual(response.status_code, 403)  # não deve ter permissão para acessar

    def test_create_invalid_profile_image_with_permission(self):
        client = create_user_and_do_authentication(permissions=["file.add_profileimage"])

        url = reverse("image-list")

        with open(PROFILE_IMAGE_INVALID_FILENAME, "rb") as invalid_image:
            # invalid_image é um arquivo txt
            profile_image_data = {"image": invalid_image}

            response = client.post(path=url, data=profile_image_data, format="multipart")

            # deve retornar um erro avisando que é um arquivo de imagem inválido
            self.assertEqual(response.status_code, 400)
            self.assertIsNotNone(response.data.get("image"))
            self.assertEqual(ProfileImage.objects.count(), 0)  # não deve ser criado no banco
