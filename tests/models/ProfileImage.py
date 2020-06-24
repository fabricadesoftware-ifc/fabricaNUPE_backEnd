from os import remove

from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image

from nupe.file.models import ProfileImage
from resources.const.datas.ProfileImage import PROFILE_IMAGE_VALID_FILENAME


class ProfileImageTestCase(TestCase):
    def test_create_valid(self):
        new_image = Image.new("RGB", (100, 100), color="blue")  # uma imagem qualquer é criada para teste
        new_image.save(PROFILE_IMAGE_VALID_FILENAME)

        with open(PROFILE_IMAGE_VALID_FILENAME, "rb") as image:
            image = ImageFile(image)

            profile_image = ProfileImage.objects.create(image=image)

            self.assertEqual(ProfileImage.objects.count(), 1)  # objeto deve ser criado no banco de dados

            remove(profile_image.image.path)  # remove o arquivo criado no diretório "media/"
            remove(PROFILE_IMAGE_VALID_FILENAME)  # a imagem criada para teste é removida
