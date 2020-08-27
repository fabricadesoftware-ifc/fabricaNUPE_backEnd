from rest_framework import serializers

from django.contrib.auth.models import User

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
