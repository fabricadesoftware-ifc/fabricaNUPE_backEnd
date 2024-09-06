from django.core.validators import MinLengthValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from nupe.core.utils.properties import calculate_age
from nupe.core.utils.regex import ONLY_NUMBERS

from uploader.models import Image

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

        account: relação inversa para a model Account

    Propriedades:
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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True, help_text="Somente números",)
    birthday_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(
        max_length=12,
        validators=[ONLY_NUMBERS, MinLengthValidator(11)],
        null=True,
        blank=True,
        help_text="DDD+Número",
    )
    profile_image = models.OneToOneField(
        Image,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        help_text="O upload da imagem deve ser feito antes, para obter o atributo de associação",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        return calculate_age(self.birthday_date)
