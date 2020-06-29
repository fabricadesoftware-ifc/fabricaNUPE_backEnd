from os import path
from shutil import rmtree

from django.test import TestCase
from model_bakery import baker

from nupe.file.models.image_upload import ProfileImageTest


class ProfileImageTestCase(TestCase):
    def tearDown(self):
        path_test_image = "media/tests"

        if path.exists(path_test_image):
            rmtree(path_test_image)

    def test_has_all_attributes(self):
        self.assertIs(hasattr(ProfileImageTest, "created_at"), True)
        self.assertIs(hasattr(ProfileImageTest, "updated_at"), True)
        self.assertIs(hasattr(ProfileImageTest, "image"), True)

    def test_return_str(self):
        profile_image = baker.make(ProfileImageTest, _create_files=True)

        self.assertEqual(str(profile_image), profile_image.url)

    def test_return_properties(self):
        profile_image = baker.make(ProfileImageTest, _create_files=True)

        self.assertEqual(profile_image.url, profile_image.image.url)
