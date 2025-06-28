from rest_framework import serializers
from calyvim.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    member_role = serializers.CharField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "description", "member_role", "created_at"]
