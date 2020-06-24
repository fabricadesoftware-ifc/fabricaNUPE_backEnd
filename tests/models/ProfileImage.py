from os import remove

from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image

from nupe.file.models import ProfileImage


class ProfileImageTestCase(TestCase):
    def test_create_valid(self):
        filename = "tests/teste.png"

        new_image = Image.new("RGB", (100, 100), color="blue")  # uma imagem qualquer é criada para teste
        new_image.save(filename)

        with open(filename, "rb") as image:
            image = ImageFile(image)

            profile_image = ProfileImage.objects.create(image=image)

            self.assertEqual(ProfileImage.objects.count(), 1)  # objeto deve ser criado no banco de dados

            remove(profile_image.image.path)  # a midia criada pelo objeto é removida
            remove(filename)  # a imagem criada para teste é removida
