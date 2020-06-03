from django.contrib.auth.models import Permission, User
from rest_framework.test import APIClient

from resources.const.datas.User import USERNAME


def create_user_with_permissions(*, username: str = USERNAME, permissions: list) -> User:
    """cria um usuário no banco com as permissões fornecidas"""
    user = User.objects.create_user(username=username, password=username)

    for permission in permissions:
        app_label, codename = permission.split(".")
        user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))

    return user


def client_force_authenticate(*, client: APIClient = APIClient(), permissions: list) -> APIClient:
    """cria um usuário no banco com as permissões fornecidas e autentica ele para as requisições futuras"""
    user = create_user_with_permissions(permissions=permissions)

    client.force_authenticate(user=user)

    return client
