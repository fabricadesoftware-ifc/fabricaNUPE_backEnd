from rest_framework.routers import SimpleRouter

from nupe.core.views import (
    AcademicEducationViewSet,
    CampusViewSet,
    CityViewSet,
    CourseViewSet,
    GradeViewSet,
    InstitutionViewSet,
    LocationViewSet,
    PersonViewSet,
    StateViewSet,
    StudentViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register("person", PersonViewSet, basename="person")
router.register("student", StudentViewSet, basename="student")
router.register("user", UserViewSet, basename="user")
router.register("institution", InstitutionViewSet, basename="institution")
router.register("campus", CampusViewSet, basename="campus")
router.register("location", LocationViewSet, basename="location")
router.register("city", CityViewSet, basename="city")
router.register("state", StateViewSet, basename="state")
router.register("course", CourseViewSet, basename="course")
router.register("grade", GradeViewSet, basename="grade")
router.register("academic_education", AcademicEducationViewSet, basename="academic_education")
