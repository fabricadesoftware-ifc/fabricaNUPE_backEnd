from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from validate_docbr import CPF

PERSON_FIRST_NAME_MAX_LENGTH = 50
PERSON_LAST_NAME_MAX_LENGTH = 100
PERSON_CPF_MAX_LENGTH = 11
PERSON_RG_MAX_LENGTH = 7
PERSON_GENDER_MAX_LENGTH = 1
PERSON_CONTACT_MAX_LENGTH = 12
GENDER_CHOICES = [("F", "Feminino"), ("M", "Masculino")]

ONLY_NUMBERS = RegexValidator(r"^[0-9]*$", message="Este campo deve conter somente números")
ONLY_LETTERS = RegexValidator(r"^[a-z A-Z]*$", message="Este campo deve conter somente letras")

INVALID_CPF_MESSAGE = "Este campo deve conter um CPF válido"


class Person(models.Model):
    first_name = models.CharField(
        max_length=PERSON_FIRST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS], verbose_name="nome"
    )
    last_name = models.CharField(
        max_length=PERSON_LAST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS], verbose_name="sobrenome"
    )
    cpf = models.CharField(max_length=PERSON_CPF_MAX_LENGTH, help_text="Somente números", unique=True)
    rg = models.CharField(
        max_length=PERSON_RG_MAX_LENGTH, help_text="Somente números", validators=[ONLY_NUMBERS], unique=True
    )
    born_date = models.DateField(verbose_name="data de nascimento")
    gender = models.CharField(max_length=PERSON_GENDER_MAX_LENGTH, choices=GENDER_CHOICES)
    contact = models.CharField(
        max_length=PERSON_CONTACT_MAX_LENGTH,
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

    def clean_fields(self, exclude=None):
        if self.first_name:
            self.first_name = self.first_name.strip()

        if self.last_name:
            self.last_name = self.last_name.strip()

        return super().clean_fields(exclude=exclude)

    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

        if self.cpf and not CPF().validate(self.cpf):
            raise ValidationError({"cpf": INVALID_CPF_MESSAGE})
