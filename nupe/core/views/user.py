from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from django.contrib.auth.models import User
from nupe.core.serializers import UserInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "id"

    queryset = User.objects.all()
    serializer_classes = {
        "retrieve": UserInfoSerializer,
    }
    default_serializer_class = UserInfoSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


    @action(
        detail=False, url_path="current",
    )
    @swagger_auto_schema(responses={200: UserInfoSerializer})
    def current(self, request):
        if not (request.user and request.user.is_authenticated):
            raise PermissionDenied()
        serializer = UserInfoSerializer(self.request.user)
        data = {"user": serializer.data}
        return Response(data)

