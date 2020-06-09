from django.core.validators import RegexValidator

from resources.const.messages.Regex import ONLY_LETTER_AND_SPACE_MESSAGE, ONLY_NUMBERS_MESSAGE

ONLY_NUMBERS = RegexValidator(r"^[0-9]*$", message=ONLY_NUMBERS_MESSAGE)
ONLY_LETTERS_AND_SPACE = RegexValidator(r"^[a-z A-Z]*$", message=ONLY_LETTER_AND_SPACE_MESSAGE)
