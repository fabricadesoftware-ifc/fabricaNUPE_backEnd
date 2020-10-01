from rest_framework.routers import SimpleRouter

from nupe.core.views import (
    AcademicEducationViewSet,
    CampusViewSet,
    CityViewSet,
    CourseViewSet,
    FunctionViewSet,
    GradeViewSet,
    InstitutionViewSet,
    LocationViewSet,
    PersonViewSet,
    SectorViewSet,
    StateViewSet,
    StudentViewSet,
)

router = SimpleRouter()

router.register("academic_education", AcademicEducationViewSet, basename="academic_education")
router.register("campus", CampusViewSet, basename="campus")
router.register("city", CityViewSet, basename="city")
router.register("course", CourseViewSet, basename="course")
router.register("function", FunctionViewSet, basename="function")
router.register("grade", GradeViewSet, basename="grade")
router.register("institution", InstitutionViewSet, basename="institution")
router.register("location", LocationViewSet, basename="location")
router.register("person", PersonViewSet, basename="person")
router.register("sector", SectorViewSet, basename="sector")
router.register("state", StateViewSet, basename="state")
router.register("student", StudentViewSet, basename="student")
