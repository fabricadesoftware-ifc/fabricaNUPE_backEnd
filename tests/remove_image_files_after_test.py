from os import path
from shutil import rmtree

from nupe.settings_test import MEDIA_ROOT


def remove_all_files_in_dir(dir: str = MEDIA_ROOT):
    """
    Por padrão, remove todos os arquivos localizado no diretório especificado em MEDIA_ROOT,
    mas é possível remover todos os arquivos de qualquer diretório passado como argumento
    """

    if path.exists(dir):
        rmtree(dir)
