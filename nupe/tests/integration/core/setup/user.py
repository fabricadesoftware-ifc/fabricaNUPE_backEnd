from django.contrib.auth.models import Permission, User
from rest_framework.test import APIClient

from nupe.resources.datas.core.user import PASSWORD, USERNAME


def create_user_with_permissions(
    *, username: str = USERNAME, password: str = PASSWORD, permissions: list = []
) -> User:
    user = User.objects.create_user(username=username, password=password)

    for permission in permissions:
        app_label, codename = permission.split(".")
        user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))

    return user


def create_user_with_permissions_and_do_authentication(
    *, username: str = USERNAME, password: str = PASSWORD, permissions: list = []
) -> APIClient:
    client = APIClient()

    user = create_user_with_permissions(username=username, password=password, permissions=permissions)
    client.force_authenticate(user=user)

    return client


def delete_all_users():
    User.objects.all().delete()
