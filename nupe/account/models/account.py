from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteManager, SafeDeleteModel


class AccountManager(BaseUserManager, SafeDeleteManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):  # pragma: no cover
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):  # pragma: no cover
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):  # pragma: no cover
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
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
    person = models.OneToOneField("core.Person", related_name="account", on_delete=models.CASCADE)
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
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.person.full_name

    @property
    def short_name(self):
        return self.person.first_name
