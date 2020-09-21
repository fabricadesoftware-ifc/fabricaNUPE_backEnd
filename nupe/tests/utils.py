import os

from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from PIL import Image

from nupe.file.models import ProfileImage
from nupe.resources.datas.file.image_upload import PROFILE_IMAGE_INVALID, PROFILE_IMAGE_PNG


def mock_profile_image(filename: str = PROFILE_IMAGE_PNG, quantity: int = 1) -> ProfileImage:
    """
    Cria uma imagem qualquer e retorna um ou mais objetos da model ProfileImage

    Retorna:
        [ProfileImage]: objeto da model
    """
    filename = create_image(filename)
    _, extension = filename.rsplit(".", 1)

    profile_images = baker.make(
        ProfileImage,
        image=SimpleUploadedFile(
            name=filename, content=open(filename, "rb").read(), content_type=f"image/{extension}"
        ),
        _quantity=quantity,
    )

    if quantity == 1:
        return profile_images[0]

    return profile_images


def create_image(filename: str = PROFILE_IMAGE_PNG) -> str:
    """
    Cria uma imagem qualquer

    Retorna:
        [str]: nome do arquivo
    """
    if not os.path.exists(filename):
        with Image.new("RGB", (50, 50), color="blue") as new_image:
            new_image.save(filename)

    return filename


def create_invalid_image():
    """
    Cria um arquivo de imagem inválido qualquer
    """
    if not os.path.exists(PROFILE_IMAGE_INVALID):
        with open(PROFILE_IMAGE_INVALID, "w") as invalid_image:
            invalid_image.write("foo bar")
