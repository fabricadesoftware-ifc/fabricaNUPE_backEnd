import os
from hashlib import sha256

from django.db import models


def make_path_profile_image(instance, filename):
    """
    Cria uma máscara para o nome do arquivo e retorna o path com o nome mascarado
    """

    filename, extension = filename.rsplit(".", 1)

    filename_hashed = sha256(filename.encode()).hexdigest()

    new_filename = f"{filename_hashed}.{extension}"

    return f"images/profiles/{new_filename}"


class ProfileImage(models.Model):
    """
    Model para guardar o path da imagem de perfil da pessoa

    Exemplo: 'media/exemplo/foo.jpeg'

    Attr:
        image: manager da imagem
        created_at: data/hora de criação
        updated_at: data/hora de atualização

    Properties:
        url: url de acesso à imagem
    """

    image = models.ImageField(upload_to=make_path_profile_image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def delete(self, using=None, keep_parents=False):
        os.remove(self.image.path)

        return super().delete(using=using, keep_parents=keep_parents)

    @property
    def url(self):
        return self.image.url
