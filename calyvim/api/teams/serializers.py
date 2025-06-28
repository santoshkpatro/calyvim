from rest_framework import serializers
from calyvim.models import Team, Organization


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "bio",
            "created_by",
            "organization_id",
        ]
