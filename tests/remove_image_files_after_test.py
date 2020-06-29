from os import path
from shutil import rmtree


def remove_all_files_in_dir(dir: str = "media/tests"):
    if path.exists(dir):
        rmtree(dir)
