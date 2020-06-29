from django.core.validators import MinLengthValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.properties import calculate_age
from nupe.core.utils.regex import ONLY_LETTERS_AND_SPACE, ONLY_NUMBERS

PERSON_FIRST_NAME_MAX_LENGTH = 50
PERSON_LAST_NAME_MAX_LENGTH = 100

PERSON_CPF_MIN_LENGTH = PERSON_CPF_MAX_LENGTH = 11

PERSON_GENDER_MAX_LENGTH = 1
PERSON_CONTACT_MIN_LENGTH = PERSON_CONTACT_MAX_LENGTH = 12


class Person(SafeDeleteModel):
    FEMININO = "F"
    MASCULINO = "M"

    GENDER_CHOICES = [
        (FEMININO, "Feminino"),
        (MASCULINO, "Masculino"),
    ]

    _safedelete_policy = SOFT_DELETE_CASCADE

    first_name = models.CharField(max_length=PERSON_FIRST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    last_name = models.CharField(max_length=PERSON_LAST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    cpf = models.CharField(
        max_length=PERSON_CPF_MAX_LENGTH, validators=[MinLengthValidator(PERSON_CPF_MIN_LENGTH)], unique=True,
    )
    birthday_date = models.DateField()
    gender = models.CharField(max_length=PERSON_GENDER_MAX_LENGTH, choices=GENDER_CHOICES)
    contact = models.CharField(
        max_length=PERSON_CONTACT_MAX_LENGTH,
        validators=[ONLY_NUMBERS, MinLengthValidator(PERSON_CONTACT_MIN_LENGTH)],
        null=True,
        blank=True,
        help_text="DDD+Número",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        return calculate_age(self.birthday_date)
