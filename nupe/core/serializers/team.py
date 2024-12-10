from rest_framework.serializers import ModelSerializer

from nupe.core.models import Team

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        depth = 1