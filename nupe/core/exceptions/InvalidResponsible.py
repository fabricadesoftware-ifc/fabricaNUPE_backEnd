from rest_framework.exceptions import APIException

from resources.const.Messages import MYSELF_RESPONSIBLE_MESSAGE, UNDER_AGE_RESPONSIBLE_MESSAGE


class InvalidResponsible(APIException):
    status_code = 400


class UnderAgeResponsible(InvalidResponsible):
    default_detail = UNDER_AGE_RESPONSIBLE_MESSAGE


class MyselfResponsible(InvalidResponsible):
    default_detail = MYSELF_RESPONSIBLE_MESSAGE
