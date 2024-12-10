from rest_framework.viewsets import ModelViewSet

from nupe.core.models import Team
from nupe.core.serializers.team import TeamSerializer

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer