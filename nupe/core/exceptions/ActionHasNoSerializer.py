from rest_framework.exceptions import APIException


class ActionHasNoSerializer(APIException):
    status_code = 501
    default_detail = "Ação não tem serializer"
    default_code = "serializer_nao_implementado"
