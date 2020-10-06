from django.contrib.auth.models import Permission
from model_bakery import baker
from rest_framework.test import APIClient

from nupe.account.models import Account
from nupe.resources.datas.account.account import EMAIL, PASSWORD


def create_account_with_permissions(
    *, email: str = EMAIL, password: str = PASSWORD, permissions: list = []
) -> Account:
    account = Account.objects.create_user(
        email=email,
        password=password,
        person=baker.make("core.Person"),
        function=baker.make("core.Function"),
        sector=baker.make("core.Sector"),
    )

    for permission in permissions:
        app_label, codename = permission.split(".")
        account.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))

    return account


def create_account_with_permissions_and_do_authentication(
    *, email: str = EMAIL, password: str = PASSWORD, permissions: list = []
) -> APIClient:
    client = APIClient()

    account = create_account_with_permissions(email=email, password=password, permissions=permissions)

    client.force_authenticate(user=account)

    return client
