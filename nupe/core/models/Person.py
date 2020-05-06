from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from validate_docbr import CPF


class Person(models.Model):
    GENDER_CHOICES = [("F", "Feminino"), ("M", "Masculino")]
    ONLY_NUMBERS = RegexValidator(r"^[0-9]*$", message="Este campo deve conter somente números")
    ONLY_LETTERS = RegexValidator(r"^[a-z A-Z]*$", message="Este campo deve conter somente letras")

    first_name = models.CharField(max_length=50, validators=[ONLY_LETTERS], verbose_name="nome")
    last_name = models.CharField(max_length=100, validators=[ONLY_LETTERS], verbose_name="sobrenome")
    cpf = models.CharField(max_length=11, help_text="Somente números", unique=True)
    rg = models.CharField(max_length=7, help_text="Somente números", validators=[ONLY_NUMBERS], unique=True)
    born_date = models.DateField(verbose_name="data de nascimento")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(
        max_length=12,
        validators=[ONLY_NUMBERS],
        verbose_name="contato",
        help_text="DDD + número",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="atualizado em", null=True, blank=True)

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def age(self):
        return timezone.now().year - self.born_date.year

    def __str__(self):
        return self.full_name

    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

        if self.cpf and not CPF().validate(self.cpf):
            raise ValidationError({"cpf": "Este campo deve conter um CPF válido"})
