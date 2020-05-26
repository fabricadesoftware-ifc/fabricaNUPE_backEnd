from nupe.core.models.Course import COURSE_MAX_LENGTH, GRADE_MAX_LENGTH, AcademicEducation, Course, Grade
from nupe.core.models.Institution import (
    CAMPUS_MAX_LENGTH,
    INSTITUTION_MAX_LENGTH,
    AcademicEducationCampus,
    Campus,
    Institution,
    InstitutionCampus,
)
from nupe.core.models.Location import CITY_MAX_LENGTH, STATE_MAX_LENGTH, City, Location, State
from nupe.core.models.Person import (
    PERSON_CONTACT_MAX_LENGTH,
    PERSON_CONTACT_MIN_LENGTH,
    PERSON_CPF_MAX_LENGTH,
    PERSON_CPF_MIN_LENGTH,
    PERSON_FIRST_NAME_MAX_LENGTH,
    PERSON_GENDER_MAX_LENGTH,
    PERSON_INVALID_CPF_MESSAGE,
    PERSON_LAST_NAME_MAX_LENGTH,
    PERSON_RG_MAX_LENGTH,
    PERSON_RG_MIN_LENGTH,
    Person,
)
from nupe.core.models.Student import (
    MYSELF_RESPONSIBLE_MESSAGE,
    RESPONSIBLE_MIN_AGE,
    STUDENT_REGISTRATION_MAX_LENGTH,
    UNDER_AGE_RESPONSIBLE_MESSAGE,
    Responsible,
    Student,
)
