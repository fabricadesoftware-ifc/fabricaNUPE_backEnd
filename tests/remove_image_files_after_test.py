from os import path
from shutil import rmtree

from django.conf import settings


def remove_all_files_in_dir(dir: str = settings.MEDIA_ROOT):
    """
    Por padrão, remove todos os arquivos localizado no diretório especificado em MEDIA_ROOT,
    mas é possível remover todos os arquivos de qualquer diretório passado como argumento
    """

    if path.exists(dir):
        rmtree(dir)
