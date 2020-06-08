from rest_framework.exceptions import APIException


class ActionNotImplemented(APIException):
    status_code = 501
    default_detail = "Ação não implementada"
