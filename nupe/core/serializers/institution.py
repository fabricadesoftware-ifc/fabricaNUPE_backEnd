from rest_framework.serializers import ModelSerializer

from nupe.core.models import Campus, Institution


class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "name"]

    def validate(self, data):
        data["name"] = data.get("name").title()

        return super().validate(data)


class CampusSerializer(ModelSerializer):
    class Meta:
        model = Campus
        fields = ["id", "name", "location", "institutions", "academic_education"]

    def validate(self, data):
        data["name"] = data.get("name").title()

        return super().validate(data)


class CampusListSerializer(ModelSerializer):
    class Meta:
        model = Campus
        fields = ["id", "name", "location"]
