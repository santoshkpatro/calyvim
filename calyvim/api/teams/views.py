from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from calyvim.models import Team
from calyvim.api.teams.serializers import TeamSerializer
from calyvim.utils.response import api_response_template


class TeamViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response_data = api_response_template()
        teams = Team.objects.filter(members__user=request.user)
        serializer = TeamSerializer(teams, many=True)
        response_data["result"] = serializer.data
        response_data["detail"] = "Teams retrieved successfully."
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        response_data = api_response_template()
        team = Team.objects.filter(id=pk, members__user=request.user).first()
        if not team:
            response_data["detail"] = "Team not found or you do not have access to it."
            response_data["error"] = "team_not_found"
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamSerializer(team)
        response_data["result"] = serializer.data
        response_data["detail"] = "Team retrieved successfully."
        return Response(data=response_data, status=status.HTTP_200_OK)
