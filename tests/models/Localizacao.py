from django.db.utils import IntegrityError
from django.test import TestCase

from nupe.core.models import Cidade, Estado, Localizacao


class LocalizacaoTestCase(TestCase):
    cidade = "Joinville"
    estado = "Santa Catarina"

    def setUp(self):
        Cidade.objects.create(nome=self.cidade)
        Estado.objects.create(nome=self.estado)

    def test_cria_localizacao(self):
        cidade1 = Cidade.objects.get(nome=self.cidade)
        estado1 = Estado.objects.get(nome=self.estado)

        localizacao = Localizacao.objects.create(cidade=cidade1, estado=estado1)

        self.assertEqual(localizacao.cidade.nome, self.cidade)
        self.assertEqual(localizacao.estado.nome, self.estado)
        self.assertEqual(Localizacao.objects.all().count(), 1)

    def test_localizacao_unique_together(self):
        cidade1 = Cidade.objects.get(nome=self.cidade)
        estado1 = Estado.objects.get(nome=self.estado)

        Localizacao.objects.create(cidade=cidade1, estado=estado1)

        with self.assertRaises(IntegrityError):
            Localizacao.objects.create(cidade=cidade1, estado=estado1)


# TODO test para cidade e estado
