from django.dispatch import receiver
from safedelete.signals import post_undelete, pre_softdelete

from nupe.core.models import AcademicEducationCampus, Student


@receiver(signal=pre_softdelete, sender=AcademicEducationCampus, dispatch_uid="academic_education_campus_pre_delete")
def academic_education_campus_pre_delete(sender, **kwargs):
    """
    todos os estudantes que tinham relação com academic education campus que foi removido
    tem seu atributo "academic_education_campus" setado como None
    """

    academic_education_campus_deleted = kwargs.get("instance")
    students = Student.objects.filter(academic_education_campus=academic_education_campus_deleted)

    if students:
        for student in students:
            student._academic_education_campus_deleted_id = academic_education_campus_deleted.id
            student.academic_education_campus = None  # aplica on_delete=models.SET_NULL
            student.save(force_update=True)


@receiver(signal=post_undelete, sender=AcademicEducationCampus, dispatch_uid="academic_education_campus_post_undelete")
def academic_education_campus_post_undelete(sender, **kwargs):
    academic_education_campus_undeleted = kwargs.get("instance")
    students = Student.objects.filter(academic_education_campus=None)

    if students:
        for student in students:
            if student._academic_education_campus_deleted_id is academic_education_campus_undeleted.id:
                student.academic_education_campus = academic_education_campus_undeleted
                student.save(force_update=True)
