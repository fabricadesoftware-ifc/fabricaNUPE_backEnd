import os
from mimetypes import guess_extension
from secrets import token_urlsafe

from django.db import models


def make_path_image(instance, _) -> str:
    """
    Define uma máscara para o path onde a imagem será armazenada e acessada

    Retorna:
        str: path com o nome mascarado
    """
    extension = guess_extension(instance.image.file.content_type)

    if extension == ".jpe":
        extension = ".jpeg"

        # if type(instance) is ProfileImage: para futuras models
    return f"images/profiles/{instance.public_id}{extension}"


class ImageQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for image in self:
            image.image.delete()


class ImageManager(models.Manager):
    def get_queryset(self):
        return ImageQuerySet(model=self.model, using=self._db)


class Image(models.Model):
    """
    Define informações sobre uma imagem para poder acessa-la

    Exemplo:
        'media/exemplo/foo.jpeg'

    Atributos:
        image: manager da imagem

        attachment_id: identificador para associar a imagem a outro objeto (uso obrigatório)

        public_id: identificador para compor o path de acesso

        uploaded_at: data/hora de criação

        updated_at: data/hora de atualização

    Propriedades:
        url: url de acesso à imagem
    """

    image = models.ImageField(upload_to=make_path_image)
    attachment_id = models.CharField(
        max_length=255,
        unique=True,
        default=token_urlsafe,
        help_text="Esse atributo é usado para fazer associação com outro objeto",
    )
    public_id = models.CharField(
        max_length=255,
        unique=True,
        default=token_urlsafe,
        help_text="Esse atributo é usado para compor a url de acesso",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ImageManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.url

    def delete(self, using=None, keep_parents=False):
        """
        Antes de remover o objeto, a imagem é removida do diretório
        """
        os.remove(self.image.path)

        return super().delete(using=using, keep_parents=keep_parents)

    @property
    def url(self):
        return self.image.url


class ProfileImage(Image):
    """
    Herda os atributos da model Image
    """

    image = models.ImageField(upload_to=make_path_image)
