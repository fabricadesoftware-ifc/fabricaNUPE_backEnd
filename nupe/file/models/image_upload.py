from os import remove
from uuid import uuid4

from django.db import models


def make_path_profile_image(instance: models.ImageField, filename: str) -> str:
    """
    Define uma máscara para o nome do arquivo da imagem

    Retorna:
        str: o path com o nome mascarado
    """

    filename, extension = filename.rsplit(".", 1)

    new_filename = f"{uuid4()}.{extension}"

    return f"images/profiles/{new_filename}"


class ProfileImage(models.Model):
    """
    Guarda o path da imagem de perfil de uma pessoa

    Exemplo:
        'media/exemplo/foo.jpeg'

    Atributos:
        image: manager da imagem

        created_at: data/hora de criação

        updated_at: data/hora de atualização

    Propriedades:
        url: url de acesso à imagem
    """

    image = models.ImageField(upload_to=make_path_profile_image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def delete(self, using=None, keep_parents=False):
        remove(self.image.path)

        return super().delete(using=using, keep_parents=keep_parents)

    @property
    def url(self):
        return self.image.url
