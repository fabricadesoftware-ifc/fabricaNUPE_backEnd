from hashlib import sha256

from django.db import models


class UploadImage(models.Model):
    # author = models.ForeignKey()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def make_path_profile_image(instance, filename):
    filename, extension = filename.rsplit(".", 1)

    string_hashed = sha256(filename.encode()).hexdigest()

    return f"images/profiles/{string_hashed}.{extension}"


class ProfileImage(UploadImage):
    image = models.ImageField(upload_to=make_path_profile_image)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.url
