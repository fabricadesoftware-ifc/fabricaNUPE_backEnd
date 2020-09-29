from rest_framework.routers import SimpleRouter

from nupe.file.views import ProfileImageViewSet

router = SimpleRouter()

router.register("profile_image", ProfileImageViewSet, basename="profile_image")
