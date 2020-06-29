from datetime import date

from django.utils import timezone


def calculate_age(birthday_date: date) -> int:
    """
    se o mês ou o dia atual for menor do que o mês ou o dia da data de nascimento, é subtraído 1 da idade
    para obter a idade atual da pessoa
    """
    today = timezone.now()

    return today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
