from os import remove

from django.core.files.images import ImageFile
from django.test import TestCase

from nupe.file.models import ProfileImage
from resources.const.datas.ProfileImage import VALID_FILE_PROFILE_IMAGE_UPLOAD_PATH


class ProfileImageTestCase(TestCase):
    def test_create_valid(self):
        with open(VALID_FILE_PROFILE_IMAGE_UPLOAD_PATH, "rb") as image:
            image = ImageFile(image)

            profile_image = ProfileImage.objects.create(image=image)

            self.assertEqual(ProfileImage.objects.count(), 1)

            remove(profile_image.image.path)
