import json
import os

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Verifica se há vulnerabilidades nas dependências do projeto, e caso tenha, imprime

    Raises:
        CommandError: Algo de errado não está certo
    """

    FILENAME = "vulnerabilities.json"

    def handle(self, *args, **options):
        try:
            os.system(f"safety check --json -o {self.FILENAME}")

            with open(f"{self.FILENAME}", "r") as vulnerabilities_file:
                content_str = vulnerabilities_file.read()
                data = json.loads(content_str)

                if data:
                    print("================\nVULNERABILIDADES\n================\n")
                    print(data)
                    os.sys.exit("\nHá vulnerabilidades nas dependências")
        except CommandError:  # noqa
            raise CommandError("Algo de errado não está certo")
