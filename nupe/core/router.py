from rest_framework.routers import SimpleRouter

from nupe.core.views import PersonViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"person", PersonViewSet, basename="person")
