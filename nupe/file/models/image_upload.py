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

    filename_hashed = sha256(filename.encode()).hexdigest()

    new_filename = f"{filename_hashed}.{extension}"

    return f"images/profiles/{new_filename}"


class ProfileImage(UploadImage):
    image = models.ImageField(upload_to=make_path_profile_image)

    def __str__(self):
        return self.url

    @property
    def url(self):
        return self.image.url
