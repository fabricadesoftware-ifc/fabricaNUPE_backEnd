from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from nupe.core.models import (
    MYSELF_RESPONSIBLE_MESSAGE,
    RESPONSIBLE_MIN_AGE,
    UNDER_AGE_RESPONSIBLE_MESSAGE,
    Person,
    Responsible,
    Student,
)


@receiver(signal=m2m_changed, sender=Responsible, dispatch_uid="student_responsibles_add")
def student_responsibles_add(sender, **kwargs):
    """
    quando adicionado um responsável para o estudante utilizando o atributo "responsibles.add()"
    é verificado se esse responsável é válido
    """

    action = kwargs.get("action")
    student_instance = kwargs.get("instance")

    if action is not None and action == "pre_add":
        pk_set = kwargs.get("pk_set")

        for pk in pk_set:
            __if_responsible_not_valid_raise(responsible_pk=pk, student_instance=student_instance)


def __if_responsible_not_valid_raise(*, responsible_pk: int, student_instance: Student) -> ValidationError:
    responsible = Person.objects.get(pk=responsible_pk)

    # o responsável não pode ser o próprio estudante se o estudante for menor de idade
    if student_instance.age < RESPONSIBLE_MIN_AGE and responsible.id is student_instance.person.id:
        raise ValidationError({"person": MYSELF_RESPONSIBLE_MESSAGE})

    # o responsável não pode ser menor de idade
    elif responsible.age < RESPONSIBLE_MIN_AGE:
        raise ValidationError({"person": UNDER_AGE_RESPONSIBLE_MESSAGE})
