import os
from shutil import rmtree

from django.conf import settings
from django.test import TestCase

from nupe.file.models.image_upload import ProfileImage
from nupe.resources.datas.file.image_upload import PROFILE_IMAGE_JPEG, PROFILE_IMAGE_PNG
from nupe.tests.utils import mock_profile_image


class ProfileImageTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        os.remove(PROFILE_IMAGE_JPEG)
        os.remove(PROFILE_IMAGE_PNG)
        rmtree(settings.MEDIA_ROOT)

    def test_has_all_attributes(self):
        self.assertIs(hasattr(ProfileImage, "image"), True)
        self.assertIs(hasattr(ProfileImage, "attachment_id"), True)
        self.assertIs(hasattr(ProfileImage, "public_id"), True)
        self.assertIs(hasattr(ProfileImage, "uploaded_at"), True)
        self.assertIs(hasattr(ProfileImage, "updated_at"), True)

    def test_return_str(self):
        mocked_image = mock_profile_image()

        self.assertEqual(str(mocked_image), mocked_image.image.url)

    def test_return_properties(self):
        mocked_image = mock_profile_image()

        self.assertEqual(mocked_image.url, mocked_image.image.url)

    def test_make_path_image_jpeg(self):
        mocked_image = mock_profile_image(filename=PROFILE_IMAGE_JPEG)
        _, extension = mocked_image.url.rsplit(".", 1)

        self.assertEqual(extension, "jpeg")

    def test_should_remove_file_on_delete(self):
        mocked_image = mock_profile_image()

        self.assertIs(os.path.exists(mocked_image.image.path), True)

        mocked_image.delete()

        # Deve ser removida do diretório
        self.assertIs(os.path.exists(mocked_image.image.path), False)

    def test_should_remove_more_than_one_file_on_delete(self):
        mocked_images = mock_profile_image(quantity=2)

        self.assertIs(os.path.exists(mocked_images[0].image.path), True)
        self.assertIs(os.path.exists(mocked_images[1].image.path), True)

        ProfileImage.objects.all().delete()

        # Devem ser removidas do diretório
        self.assertIs(os.path.exists(mocked_images[0].image.path), False)
        self.assertIs(os.path.exists(mocked_images[1].image.path), False)
