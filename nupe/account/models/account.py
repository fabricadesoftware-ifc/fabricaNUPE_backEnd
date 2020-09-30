from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class Account(AbstractUser, SafeDeleteModel):
    """
    Define as informações da conta de um usuário do sistema

    Exemplo:
        'nupexample@example.com, nupe example, IFC Araquari'

    Atributos:
        _safedelete_policy: SOFT_DELETE_CASCADE

        email: identificação para login

        person: identificador para o objeto da model Person com as informações pessoais

        local_job: identificador para o objeto da model InstitutionCampus com o local de trabalho

        function: identificador para o objeto da model Function com a função do funcionário

        sector: identificador para o objeto da model Sector com o setor onde o funcionário trabalha

        date_joined: data da criação da conta

        updated_at: data/hora da última atualização da conta

        is_active: booleano para status da conta, ativa/não ativa

        is_staff: booleano para status de funcionário, é/não é

        is_superuser: boolean para status de administrador do sistema, é/não é

    Propriedades:
        full_name: nome completo do usuário

        short_name: primeiro nome do usuário
    """

    _safedelete_policy = SOFT_DELETE_CASCADE  # mascara os objetos relacionados

    email = models.EmailField(unique=True)
    person = models.OneToOneField("core.Person", related_name="account", on_delete=models.CASCADE, null=True)
    local_job = models.ForeignKey(
        "core.InstitutionCampus",
        related_name="workers",
        related_query_name="worker",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    function = models.ForeignKey(
        "core.Function", related_name="workers", related_query_name="worker", on_delete=models.CASCADE
    )
    sector = models.ForeignKey(
        "core.Sector", related_name="workers", related_query_name="worker", on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        if self.person is not None:
            return self.person.full_name

        return None

    @property
    def short_name(self):
        if self.person is not None:
            return self.person.first_name

        return None
