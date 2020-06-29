from django.test import TestCase
from model_bakery import baker

from nupe.file.models import ProfileImage


class ProfileImageTestCase(TestCase):
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
