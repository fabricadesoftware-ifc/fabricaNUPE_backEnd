from rest_framework.exceptions import APIException


class ActionNotImplemented(APIException):
    """
    Exceção para o caso de uma view utilizar uma ação que não tenha um serializer associado a ela
    """

    status_code = 501
    default_detail = "Ação não implementada"
