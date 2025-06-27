from rest_framework import serializers
from calyvim.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "bio",
            "created_by",
        ]
