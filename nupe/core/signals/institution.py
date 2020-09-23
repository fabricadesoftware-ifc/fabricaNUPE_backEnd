from django.dispatch import receiver
from safedelete.signals import post_undelete, pre_softdelete

from nupe.core.models import AcademicEducationInstitutionCampus, Student


@receiver(
    signal=pre_softdelete,
    sender=AcademicEducationInstitutionCampus,
    dispatch_uid="academic_education_institution_campus_pre_delete",
)
def academic_education_institution_campus_pre_delete(sender, **kwargs):
    """
    Quando um objeto da model AcademicEducationInstitutionCampus é removido, todos os estudantes que tem relação com
    essa model tem seu atributo 'academic_education_institution_campus' setado como 'None'
    """

    academic_education_institution_campus_deleted = kwargs.get("instance")
    students = Student.objects.filter(
        academic_education_institution_campus=academic_education_institution_campus_deleted
    )

    for student in students:
        # armazena o id do objeto removido para caso seja restaurado, consiga atualizar o atributo com
        # o valor anterior corretamente
        student._academic_education_institution_campus_deleted_id = academic_education_institution_campus_deleted.id
        student.academic_education_institution_campus = None  # aplica on_delete=models.SET_NULL
        student.save(force_update=True)


@receiver(
    signal=post_undelete,
    sender=AcademicEducationInstitutionCampus,
    dispatch_uid="academic_education_institution_campus_post_undelete",
)
def academic_education_institution_campus_post_undelete(sender, **kwargs):
    """
    Quando um objeto da model AcademicEducationInstitutionCampus é restaurado, todos os estudantes que tem relação com
    essa model tem seu atributo 'academic_education_institution_campus' setado como o valor anterior a remoção
    """

    academic_education_institution_campus_undeleted = kwargs.get("instance")
    students = Student.objects.filter(academic_education_institution_campus__isnull=True)

    for student in students:
        if (
            student._academic_education_institution_campus_deleted_id
            is academic_education_institution_campus_undeleted.id
        ):
            student.academic_education_institution_campus = academic_education_institution_campus_undeleted
            student.save(force_update=True)
