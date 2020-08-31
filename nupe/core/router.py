from rest_framework.routers import SimpleRouter

from nupe.core.views import PersonViewSet, StudentViewSet, UserViewSet

router = SimpleRouter()
router.register("person", PersonViewSet, basename="person")
router.register("student", StudentViewSet, basename="student")
router.register("user", UserViewSet, basename="user")
