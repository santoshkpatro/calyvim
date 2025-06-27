from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from calyvim.views import index
from calyvim.api.accounts.views import AccountViewSet
from calyvim.api.teams.views import TeamViewSet

api_router = SimpleRouter(trailing_slash=False)

api_router.register("accounts", AccountViewSet, basename="account")
api_router.register("teams", TeamViewSet, basename="team")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    re_path(r"^(?:.*)/?$", index, name="index"),  # Catch-all route
]
