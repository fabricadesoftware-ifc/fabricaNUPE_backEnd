from rest_framework.routers import SimpleRouter

from nupe.core.views import PersonViewSet

router = SimpleRouter()
router.register("person", PersonViewSet, basename="person")
