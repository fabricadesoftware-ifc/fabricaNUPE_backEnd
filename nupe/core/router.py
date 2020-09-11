from rest_framework.routers import SimpleRouter

from nupe.core.views import CampusViewSet, InstitutionViewSet, PersonViewSet, StudentViewSet, UserViewSet

router = SimpleRouter()
router.register("person", PersonViewSet, basename="person")
router.register("student", StudentViewSet, basename="student")
router.register("user", UserViewSet, basename="user")
router.register("institution", InstitutionViewSet, basename="institution")
router.register("campus", CampusViewSet, basename="campus")
