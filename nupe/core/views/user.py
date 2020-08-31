from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from nupe.core.serializers import UserCurrentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCurrentSerializer

    @action(
        detail=False, url_path="current",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: UserCurrentSerializer})
    def current(self, request):
        serializer = UserCurrentSerializer(data=self.request.user)
        data = {"user": serializer.data}

        return Response(data)
