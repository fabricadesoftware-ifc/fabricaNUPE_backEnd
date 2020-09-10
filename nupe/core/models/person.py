from django.core.validators import MinLengthValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.properties import calculate_age
from nupe.core.utils.regex import ONLY_LETTERS_AND_SPACE, ONLY_NUMBERS

PERSON_FIRST_NAME_MAX_LENGTH = 50
PERSON_LAST_NAME_MAX_LENGTH = 100

PERSON_CPF_MIN_LENGTH = PERSON_CPF_MAX_LENGTH = 11

PERSON_GENDER_MAX_LENGTH = 1
PERSON_CONTACT_MIN_LENGTH = 11
PERSON_CONTACT_MAX_LENGTH = 12


class Person(SafeDeleteModel):
    """
    Define as informações pessoais de uma pessoa, seja ela um estudante, usuário do sistema ou
    responsável de um aluno

    Exemplo:
        'Luis Guerreiro, 12345678910, 14/02/1999, M, 47 988887777'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        first_name: primeiro nome da pessoa

        last_name: sobrenome da pessoa

        cpf: número do documento 'Cadastro de Pessoas Físicas' (somente números)

        birthday_date: data de nascimento (yyyy-mm-dd)

        gender: sexo (F, M)

        contact: número de contato (DDD+Número)

        profile_image: url de acesso para a foto de perfil

        created_at: data do cadastro

        updated_at: data da última atualização das informações

        student_registrations: relação inversa para a model Student

        dependents: relação inversa para a model Student

        responsibles: relação inversa para a model Responsible

    Properties:
        full_name: nome completo da pessoa

        age: idade da pessoa
    """

    FEMININO = "F"
    MASCULINO = "M"

    GENDER_CHOICES = [
        (FEMININO, "Feminino"),
        (MASCULINO, "Masculino"),
    ]

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    first_name = models.CharField(max_length=PERSON_FIRST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    last_name = models.CharField(max_length=PERSON_LAST_NAME_MAX_LENGTH, validators=[ONLY_LETTERS_AND_SPACE])
    cpf = models.CharField(
        max_length=PERSON_CPF_MAX_LENGTH,
        validators=[MinLengthValidator(PERSON_CPF_MIN_LENGTH)],
        unique=True,
        help_text="Somente números",
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
    profile_image = models.OneToOneField(
        "file.ProfileImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="O upload da imagem deve ser feito antes, para obter o atributo de associação",
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
