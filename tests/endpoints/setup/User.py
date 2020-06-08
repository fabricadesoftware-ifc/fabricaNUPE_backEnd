from django.contrib.auth.models import Permission, User
from rest_framework.test import APIClient

from resources.const.datas.User import USERNAME


def create_user_with_permissions(*, username: str = USERNAME, permissions: list) -> User:
    user = User.objects.create_user(username=username, password=username)

    for permission in permissions:
        app_label, codename = permission.split(".")
        user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))

    return user


def create_user_and_do_authentication(permissions: list) -> APIClient:
    client = APIClient()

    user = create_user_with_permissions(username="teste", permissions=permissions)
    client.force_authenticate(user=user)

    return client
