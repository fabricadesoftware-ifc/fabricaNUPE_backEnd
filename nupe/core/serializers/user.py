from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class CurrentUserSerializer(ModelSerializer):
    """
    Retorna informações sobre o usuário logado atual

    Campos:
        id: identificador

        first_name: nome

        last_name: sobrenome
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
