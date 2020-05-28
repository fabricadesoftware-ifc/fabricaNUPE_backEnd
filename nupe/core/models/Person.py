from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from validate_docbr import CPF

from nupe.core.utils.Regex import ONLY_LETTERS_AND_SPACE, ONLY_NUMBERS

PERSON_FIRST_NAME_MAX_LENGTH = 50
PERSON_LAST_NAME_MAX_LENGTH = 100

PERSON_CPF_MIN_LENGTH = PERSON_CPF_MAX_LENGTH = 11
PERSON_RG_MIN_LENGTH = PERSON_RG_MAX_LENGTH = 7

PERSON_GENDER_MAX_LENGTH = 1
PERSON_CONTACT_MIN_LENGTH = PERSON_CONTACT_MAX_LENGTH = 12
GENDER_CHOICES = [("F", "Feminino"), ("M", "Masculino")]

PERSON_INVALID_CPF_MESSAGE = "Este campo deve conter um CPF válido"


class Person(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    first_name = models.CharField(max_length=PERSON_FIRST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    last_name = models.CharField(max_length=PERSON_LAST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    cpf = models.CharField(
        max_length=PERSON_CPF_MAX_LENGTH, validators=[MinLengthValidator(PERSON_CPF_MIN_LENGTH)], unique=True,
    )
    rg = models.CharField(
        max_length=PERSON_RG_MAX_LENGTH,
        validators=[ONLY_NUMBERS, MinLengthValidator(PERSON_RG_MIN_LENGTH)],
        unique=True,
    )
    birthday_date = models.DateField()
    gender = models.CharField(max_length=PERSON_GENDER_MAX_LENGTH, choices=GENDER_CHOICES)
    contact = models.CharField(
        max_length=PERSON_CONTACT_MAX_LENGTH,
        validators=[ONLY_NUMBERS, MinLengthValidator(PERSON_CONTACT_MIN_LENGTH)],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        return timezone.now().year - self.birthday_date.year

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
            raise ValidationError({"cpf": PERSON_INVALID_CPF_MESSAGE})
