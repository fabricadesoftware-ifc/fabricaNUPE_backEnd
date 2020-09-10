import os

from nupe.file.models import Image


class ImageUploadService:
    def remove_file(self, instance):
        """
        Remove a imagem do diretório

        Argumentos:
            instance (Image): instância da model Image
        """
        if isinstance(instance, Image):
            os.remove(instance.image.path)
        else:
            raise ValueError(Image)
