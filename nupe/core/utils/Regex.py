from django.core.validators import RegexValidator

ONLY_NUMBERS = RegexValidator(r"^[0-9]*$", message="Este campo deve conter somente números")
ONLY_LETTERS_AND_SPACE = RegexValidator(r"^[a-z A-Z]*$", message="Este campo deve conter somente letras")
