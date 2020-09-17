from django.core.validators import RegexValidator

from nupe.resources.const.messages.regex import ONLY_NUMBERS_MESSAGE

ONLY_NUMBERS = RegexValidator(r"^[0-9]*$", message=ONLY_NUMBERS_MESSAGE)
