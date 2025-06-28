from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from calyvim.views import index
from calyvim.api.accounts.views import AccountViewSet
from calyvim.api.teams.views import TeamViewSet
from calyvim.api.organizations.views import OrganizationViewSet

api_router = SimpleRouter(trailing_slash=False)

api_router.register("accounts", AccountViewSet, basename="account")
api_router.register("teams", TeamViewSet, basename="team")
api_router.register("organizations", OrganizationViewSet, basename="organization")

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    re_path(r"^app/(?:.*)/?$", index, name="index"),  # Catch all routes starting with app/
]
