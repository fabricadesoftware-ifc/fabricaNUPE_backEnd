from django.test import TestCase
from model_bakery import baker

from nupe.file.models.image_upload import ProfileImage
from tests.remove_image_files_after_test import remove_all_files_in_dir


class ProfileImageTestCase(TestCase):
    def tearDown(self):
        remove_all_files_in_dir()

    def test_has_all_attributes(self):
        self.assertIs(hasattr(ProfileImage, "created_at"), True)
        self.assertIs(hasattr(ProfileImage, "updated_at"), True)
        self.assertIs(hasattr(ProfileImage, "image"), True)

    def test_return_str(self):
        profile_image = baker.make(ProfileImage, _create_files=True)

        self.assertEqual(str(profile_image), profile_image.url)

    def test_return_properties(self):
        profile_image = baker.make(ProfileImage, _create_files=True)

        self.assertEqual(profile_image.url, profile_image.image.url)
