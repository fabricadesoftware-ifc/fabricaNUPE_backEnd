from django.db import models


class Base(models.Model):
    nome = models.CharField(max_length=50, unique=True)


class Cidade(Base):
    def __str__(self):
        return self.nome


class Estado(Base):
    cidades = models.ManyToManyField(
        Cidade, related_name="estados", related_query_name="estado", through="Localizacao"
    )

    def __str__(self):
        return self.nome


class Localizacao(models.Model):
    cidade = models.ForeignKey(
        Cidade, related_name="localizacoes", related_query_name="localizacao", on_delete=models.PROTECT
    )
    estado = models.ForeignKey(
        Estado, related_name="localizacoes", related_query_name="localizacao", on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ["cidade", "estado"]
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def __str__(self):
        return "Cidade: {} | Estado: {}".format(self.cidade, self.estado)
