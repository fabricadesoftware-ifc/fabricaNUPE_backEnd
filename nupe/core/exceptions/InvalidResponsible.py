from rest_framework.exceptions import APIException

UNDER_AGE_RESPONSIBLE_MESSAGE = "O estudante deve conter um responsável maior de idade"
MYSELF_RESPONSIBLE_MESSAGE = "O estudante deve conter um responsável diferente de sí"


class InvalidResponsible(APIException):
    status_code = 400
    default_code = "responsavel_invalido"


class UnderAgeResponsible(InvalidResponsible):
    default_detail = UNDER_AGE_RESPONSIBLE_MESSAGE


class MyselfResponsible(InvalidResponsible):
    default_detail = MYSELF_RESPONSIBLE_MESSAGE
