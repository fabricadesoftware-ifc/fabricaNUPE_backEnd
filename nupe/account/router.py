from rest_framework.routers import SimpleRouter

from nupe.account.views import AccountViewSet

router = SimpleRouter()

router.register("account", AccountViewSet, basename="account")
