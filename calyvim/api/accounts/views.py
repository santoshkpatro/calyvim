from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import login
from django.utils import timezone
from django.db import transaction
from django.db.models import OuterRef, Subquery

from calyvim.api.accounts.serializers import (
    LoginSerializer,
    LoggedInUserSerializer,
    RegisterSerializer,
    TeamSerializer,
)
from calyvim.utils.response import api_response_template
from calyvim.models import User, Organization, Team, TeamMember


class AccountViewSet(ViewSet):

    # POST: /api/accounts/login
    @action(detail=False, methods=["post"], url_path="login")
    def login_action(self, request, *args, **kwargs):
        response_data = api_response_template()
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.active_objects.filter(email=email).first()
        if not user:
            response_data["detail"] = "No user found with this email"
            response_data["error"] = "user_not_found"
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            response_data["detail"] = "Incorrect password"
            response_data["error"] = "incorrect_password"
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        if user.password_expired:
            response_data["detail"] = "Password expired, please reset your password"
            response_data["error"] = "password_expired"
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        login(request, user)
        user.last_login_at = timezone.now()
        user.last_login_ip = request.META.get("REMOTE_ADDR")
        user.save(update_fields=["last_login_at", "last_login_ip"])

        logged_in_user_serializer = LoggedInUserSerializer(user)
        response_data["detail"] = "Login successful"
        response_data["result"] = logged_in_user_serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

    # POST: /api/accounts/register
    @action(detail=False, methods=["post"], url_path="register")
    def register_action(self, request, *args, **kwargs):
        response_data = api_response_template()
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user_data = serializer.validated_data
        existing_user = User.objects.filter(email=new_user_data["email"]).first()

        if existing_user and existing_user.date_joined is not None:
            response_data["detail"] = "User with this email already exists"
            response_data["error"] = "user_already_exists"
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        password = new_user_data.pop("password")
        organization = new_user_data.pop("organization")
        if existing_user:
            existing_user.set_password(password)
            existing_user.full_name = new_user_data["full_name"]
            user = existing_user
        else:
            user = User(**new_user_data)
            user.set_password(password)

        try:
            with transaction.atomic():
                user.date_joined = timezone.now()
                user.save()

                org = Organization.objects.create(name=organization, created_by=user)
                Team.objects.create(
                    organization=org, name=f"{org.name}'s Default Team", created_by=user
                )
        except Exception as e:
            response_data["detail"] = "Error creating user"
            response_data["error"] = str(e)
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Send verification email.

        response_data["detail"] = "Registration successful"
        return Response(response_data, status=status.HTTP_201_CREATED)

    # GET: /api/accounts/me
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request, *args, **kwargs):
        response_data = api_response_template()
        user = request.user
        data = {"is_authenticated": False, "user": None}

        if not user.is_authenticated:
            response_data["detail"] = "User not authenticated"
            response_data["result"] = data
            return Response(response_data, status=status.HTTP_200_OK)

        teams = (
            Team.objects.filter(members__user=user)
            .select_related("organization")
            .annotate(
                member_role=Subquery(
                    TeamMember.objects.filter(team=OuterRef("pk"), user=user).values(
                        "role"
                    )[:1]
                )
            )
        )

        print("Teams", teams[0].member_role)

        logged_in_user_serializer = LoggedInUserSerializer(user)
        team_serializer = TeamSerializer(teams, many=True)

        data["is_authenticated"] = True
        data["user"] = logged_in_user_serializer.data
        data["teams"] = team_serializer.data

        response_data["result"] = data
        response_data["detail"] = "User is logged in"
        return Response(response_data, status=status.HTTP_200_OK)
