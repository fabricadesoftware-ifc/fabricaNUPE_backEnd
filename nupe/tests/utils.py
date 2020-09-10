import os
from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from PIL import Image

from nupe.resources.const.datas.image_upload import PROFILE_IMAGE_INVALID, PROFILE_IMAGE_PNG


def remove_all_files_in_dir(dir: str = settings.MEDIA_ROOT):
    """
    Por padrão, remove todos os arquivos localizado no diretório especificado em MEDIA_ROOT,
    mas é possível remover todos os arquivos de qualquer diretório passado como argumento
    """
    if os.path.exists(dir):  # pragma: no cover
        rmtree(dir)


def mock_image(filename: str = PROFILE_IMAGE_PNG):
    """
    Cria uma imagem qualquer e retorna um objeto da model ProfileImage

    Retorna:
        [ProfileImage]: objeto da model
    """
    filename = create_image(filename)
    _, extension = filename.rsplit(".", 1)

    return baker.make(
        "file.ProfileImage",
        image=SimpleUploadedFile(
            name=filename, content=open(filename, "rb").read(), content_type=f"image/{extension}"
        ),
    )


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
    if not os.path.exists(PROFILE_IMAGE_INVALID):  # pragma: no cover
        with open(PROFILE_IMAGE_INVALID, "w") as invalid_image:
            invalid_image.write("foo bar")


def remove_images(paths: list):
    """
    Remove as imagens criadas em "create_image" e "create_invalid_image"
    """
    for path in paths:
        os.remove(path)
