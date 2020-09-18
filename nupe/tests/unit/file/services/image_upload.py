from django.test import TestCase
from model_bakery import baker

from nupe.file.services import ImageUploadService


class ProfileImageTestCase(TestCase):
    def test_invalid_remove_file_service(self):
        invalid_instace = baker.make("core.Person")

        image_service = ImageUploadService()

        with self.assertRaises(ValueError):
            image_service.remove_file(instance=invalid_instace)
