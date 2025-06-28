from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import OuterRef, Subquery

from calyvim.models import Organization, OrganizationMember
from calyvim.api.organizations.serializers import OrganizationSerializer
from calyvim.utils.response import api_response_template


class OrganizationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response_data = api_response_template()
        organizations = Organization.objects.filter(
            members__user=request.user
        ).annotate(
            member_role=Subquery(
                OrganizationMember.objects.filter(
                    organization=OuterRef("id"), user=request.user
                ).values("role")[:1]
            )
        )
        serializer = OrganizationSerializer(organizations, many=True)

        response_data["result"] = serializer.data
        response_data["detail"] = "Fetched organizations data successfully!"
        return Response(data=response_data, status=status.HTTP_200_OK)
